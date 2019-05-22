import pandas as pd
import numpy as np
import os
import glob
import Config as cn
import re
import os
import datetime
import pdb
class DataPreparation:
    def __init__(self):
        self.prepareLocalWeather()
        self.preparePower()
        self.preparePower(powerPath = cn.MeterTwoPath, fileName = 'meterTwo.csv')
        self.prepareExternalWMSGFS()
        self.updateHistoricalGFS()
        pass
    


    def prepareLocalWeather(self):
        fileslist = os.listdir(cn.LocalWMSPath)
        filePath = os.path.join(cn.PreparedLocalWMSPath,'UpdatedLocalWMS.xlsx')
        localWMSData = pd.DataFrame()
        if not 'UpdatedLocalWMS.xlsx' in os.listdir(cn.PreparedLocalWMSPath):
            
            for file in fileslist:
                
                try:
                    path = os.path.join(cn.LocalWMSPath,file)
                    data = self.formatLocalWMS(file, path)
                    localWMSData = pd.concat([localWMSData, data], axis = 0)
                    
                except:
                    pass
            localWMSData = localWMSData[cn.localWMSCols]    
        else:
            print('entering domain')
            filename = 'Todays Clean Energy,Barod_WMSData_'
            Current_Date = str(pd.Timestamp(datetime.date.today()))[0:10]
            Current_Date = re.sub("-", "_", Current_Date)
            file = filename+Current_Date+'.xls'
            path = os.path.join(cn.LocalWMSPath,file)
            data = self.formatLocalWMS(file, path)
            oldData = pd.read_excel(filePath)
            #pdb.set_trace()
            data = data[cn.localWMSCols]
            localWMSData = pd.concat([oldData, data], axis = 0)
            #pdb.set_trace()
            
        localWMSData.dropna(inplace = True)
        localWMSData.drop_duplicates(inplace = True)
        localWMSData.reset_index(inplace = True, drop = True)
        localWMSData = localWMSData.sort_values(by=['DateTime'])
        
        localWMSData.to_excel(filePath)
        
        return 0
    

    
    
    def checkLocalandExternal(self):
        return 0
    
    
    def formatLocalWMS(self,file, path):
        data = pd.read_excel(path, skiprows = 2)
        data.drop(0,axis =0, inplace = True)
        data.reset_index(inplace = True, drop = True)
        sen = re.findall(r'\d+', file)
        sen = '-'.join(sen)
        date = []
        for i in range(len(data)):
            date.append(sen)
        data['Date'] = pd.Series(date)
        data['Time Stamp'] = pd.Series([str(data.loc[i,'Time Stamp']) for i in range(0,len(data))])
        data['DateTime'] = pd.to_datetime(data['Date']+' '+data['Time Stamp'])


        return data    
        
    
    def preparePower(self, powerPath = cn.MeterOnePath, fileName = 'meterOne.csv'):
        powerMeter = pd.DataFrame()
        files = os.listdir(powerPath)
        if not fileName in os.listdir(cn.PreparedPowerPath):
            for file in files:
                path = os.path.join(powerPath,file)
                df = pd.read_csv(path, skiprows = 4)
                df.reset_index(inplace = True, drop = True)
                cols = ['ReadTime','Power']
                df = df[cols]
                df.dropna(inplace = True)
                sen = re.findall(r'\d+', file)
                sen = '-'.join(sen)
                if fileName != 'meterOne.csv':
                    sen = sen[2:]
                else:
                    pass
               
                date = []
                for i in range(len(df)):
                        date.append(sen)
                df['Date'] = pd.Series(date)
                df['ReadTime'] = pd.Series([str(df.loc[i,'ReadTime']) for i in range(0,len(df))])
                df['DateTime'] = pd.to_datetime(df['Date']+' '+df['ReadTime'])
                powerMeter = pd.concat([powerMeter,df] , axis = 0)
                powerMeter.dropna(inplace = True)
                powerMeter.reset_index(inplace = True, drop = True)
            savePath = os.path.join(cn.PreparedPowerPath, fileName)
            powerMeter = powerMeter.sort_values(by=['DateTime'])
            powerMeter = powerMeter[cn.powerCols]
            powerMeter.to_csv(savePath)
            
        else:
            if fileName == 'meterOne.csv':
               filename =  'Todays Clean Energy,BarodCSVMeter_Data_'
            else:   
                filename = 'Todays Clean Energy,BarodCSVMeter2_Data_'
            Current_Date = str(pd.Timestamp(datetime.date.today()))[0:10]
            Current_Date = re.sub("-", "_", Current_Date)
            file = filename+Current_Date+'.csv'
            path = os.path.join(powerPath,file)
            df = pd.read_csv(path, skiprows = 4)
            #pdb.set_trace()
            cols = ['ReadTime','Power']
            df = df[cols]
            df.drop_duplicates(inplace = True)
            df.dropna(inplace = True)
            df.reset_index(inplace = True, drop = True)
            sen = re.findall(r'\d+', file)
            sen = '-'.join(sen)
            if fileName != 'meterOne.csv':
                    sen = sen[2:]
            else:
                    pass
               
            date = []
            #pdb.set_trace()
            for i in range(len(df)):
                        date.append(sen)
            df['Date'] = pd.Series(date)
            df['ReadTime'] = pd.Series([str(df.loc[i,'ReadTime']) for i in range(len(df))])
            df['DateTime'] = pd.to_datetime(df['Date']+' '+df['ReadTime'])
            oldfile = os.path.join(cn.PreparedPowerPath,fileName)
            oldData = pd.read_csv(oldfile)
            #pdb.set_trace()
            df = df[cn.powerCols]
            oldData = oldData[cn.powerCols]
            oldData['DateTime'] = pd.to_datetime(oldData['DateTime'])
            powerMeter = pd.concat([oldData,df] , axis = 0)
            powerMeter.dropna(inplace = True)
            powerMeter.reset_index(inplace = True, drop = True)
            savePath = os.path.join(cn.PreparedPowerPath, fileName)
            powerMeter = powerMeter.sort_values(by=['DateTime'])
            powerMeter = powerMeter[cn.powerCols]
            powerMeter.drop_duplicates(inplace = True)
            powerMeter.to_csv(savePath)
            

    def prepareExternalWeather(self, date = None, time = None):
        histDataPath = os.path.join(cn.PreparedPowerPath,'Historical_external_WMS.csv')
        if 'Historical_external_WMS.csv' not in os.listdir(cn.PreparedPowerPath):
            print('no historical external WMS data found, please download it\n')
        else:    
            #pdb.set_trace()
            histWMSData = pd.read_csv(histDataPath)
            histWMSData = histWMSData[cn.ExternalWMSCols]
            #wantedCols = histWMSData.columns.values
            fileName = 'ExternalWMS_'+date+'_'+time+'.csv'
            path = os.path.join(cn.ExternalWMSPath, fileName)
            currentdata = pd.read_csv(path)
            currentdata = currentdata[cn.ExternalWMSCols]
            ### Remove todays historical data #######
            
            histWMSData = pd.concat([histWMSData,currentdata], axis = 0)
            
            histWMSData.drop_duplicates(inplace = True)
            
            histWMSData.reset_index(drop = True, inplace = True)
            
            
            #histWMSData = histWMSData[wantedCols]
            histWMSData['Date_DD_MM_YYYY'] = pd.to_datetime(histWMSData['Date_DD_MM_YYYY'])
            histWMSData.to_csv(histDataPath)
            
            
        return histWMSData

    def interpolateExternalWMS(self, df = None):
        
        
        date_rng = pd.Series(pd.date_range(start='1/1/2018', end='1/2/2018', freq='H')[0:-1])
        date_rng = pd.Series([str(date_rng.loc[i]).split(' ')[1] for i in range(len(date_rng))])
        interpolatedWeatData = pd.DataFrame()
        for date in df['Date_DD_MM_YYYY'].unique():
            weatData = df[df['Date_DD_MM_YYYY'] == str(date)]
            weatData.reset_index(inplace = True, drop = True)
            
            weatData['DateTime'] = pd.Series([weatData.loc[i,'Date_DD_MM_YYYY'].strftime('%Y-%m-%d')+' '+date_rng[i] for i in range(min(len(weatData),24))])
            #pdb.set_trace()
            cols = ['Wind_Chill','Cloud_Cover_Percentage','Humidity_Percentage','Precipitation','Pressure',
                    'Ambient_Temp','Visibility','Wind_Direction','Wind_Speed','DateTime']
            weatData = weatData[cols]
            weatData['DateTime'] = pd.to_datetime(weatData['DateTime'])
            weatData = weatData[0:24]
            weatData.set_index('DateTime', inplace = True)
            weatData = weatData.resample('15Min').interpolate(method = 'linear')
            
            interpolatedWeatData = pd.concat([interpolatedWeatData,weatData], axis = 0)
        interpolatedWeatData.reset_index(inplace = True)
        self.interpolatedWeatData = interpolatedWeatData.copy()
        savePath = os.path.join(cn.PreparedPowerPath,'interpolatedExternalWMS.csv')
        self.interpolatedWeatData.to_csv(savePath)
        pass
        


    def prepareExternalWMSGFS(self):
        wmspath = os.path.join(cn.PreparedPowerPath,'interpolatedExternalWMS.csv')
        WMSdata = pd.read_csv(wmspath)
        gfspath = os.path.join(cn.ExternalGFSPath,'HistoricalGFS.csv')
        GFSdata = pd.read_csv(gfspath)
        #WMSdata.drop(columns = 'Unnamed: 0', inplace = True)
        resDf = pd.merge(WMSdata, GFSdata[cn.GFScols], left_on = 'DateTime', right_on = 'DateTime', how = 'inner')
        resDf.drop_duplicates(inplace = True)
        #cols = ['dhi', 'dni', 'ghi']
        for col in cn.Roundoffcols:
            resDf[col] = round(resDf[col],2)
            
        resDf.drop_duplicates(inplace = True)
        self.ExternalWMSGFSData = resDf
        savePath = os.path.join(cn.ExternalWMSPath,'ExternalWMSGFS.csv')
        print('savepath is {}'.format(savePath))
        resDf.to_csv(savePath)
        
        
        pass
    
    def updateHistoricalGFS(self):
        externalGFSPath = os.path.join(cn.ExternalGFSPath,'ExternalGFS.csv')
        externalGFSData = pd.read_csv(externalGFSPath)
        historicalGFSPath = os.path.join(cn.ExternalGFSPath,'HistoricalGFS.csv')
        historicalGFSData = pd.read_csv(historicalGFSPath)        
        cols = ['DateTime','ghi','dni','dhi']
        externalGFSData = externalGFSData[cols]
        historicalGFSData = historicalGFSData[cols]
        #pdb.set_trace()
        df = pd.concat([historicalGFSData,externalGFSData], axis = 0)
        df.to_csv(historicalGFSPath)
        pass