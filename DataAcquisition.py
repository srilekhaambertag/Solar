### import files ##########

import pandas as pd
import pdb
import numpy as np
import os
import glob
from SaveFiles import SaveFiles
import Config as cn
import datetime
import json 
import urllib.request as ur
from pvlib.forecast import GFS

class DataAcquisition:
    def __init__(self):
        self.downloadlocalWMS()
        self.downloadPowerMeterOne()
        self.downloadPowerMeterTwo()
        self.downloadExternalWMS()
        self.downloadExternalGFS()

    
    
    def downloadlocalWMS(self):
        save = SaveFiles()
        if not os.listdir(cn.LocalWMSPath):
            save.saveLocalWMSFromFTP(downloadall = True)
        else:
            save.saveLocalWMSFromFTP()
        return 0 
    
    
    def downloadPowerMeterOne(self):
        save = SaveFiles()
        if not os.listdir(cn.MeterOnePath):
            save.savePowerFromFTP(downloadall = True)
        else:
            save.savePowerFromFTP()
        return 0 
    
    
    def downloadPowerMeterTwo(self):
        save = SaveFiles()
        if not os.listdir(cn.MeterTwoPath):
            save.savePowerFromFTP(downloadall = True,power = 'BarodCSVMeter2', savePath = cn.MeterTwoPath,
                         filename = 'Todays Clean Energy,BarodCSVMeter2_Data_')
        else:
            save.savePowerFromFTP(power = 'BarodCSVMeter2', savePath = cn.MeterTwoPath,
                         filename = 'Todays Clean Energy,BarodCSVMeter2_Data_')
        return 0 
    
    
    def downloadExternalWMS(self):
        now = str(datetime.datetime.now())
        Run_time = now[11:16]
        response = ur.urlopen("http://api.worldweatheronline.com/premium/v1/weather.ashx?key=d9235f001e83423ab2a54330192504&q=Barod&format=json&num_of_days=5&tp=1#hourly").read()
        data = json.loads(response.decode('utf-8'))
        all_data=data['data']
        if Run_time == '23:00':
            Current_day = all_data['weather'][1]
        else:
            Current_day = all_data['weather'][0]
        Current_date = Current_day['date']
        
        ################all 24 readings###############
        Hours = list(range(24))
        WMS_Data =[]
        Sunrise_time = Current_day['astronomy'][0]['sunrise']
        Sunset_time = Current_day['astronomy'][0]['sunset']
        for i in Hours:
            Time = Current_day['hourly'][i]['time']
            Wind_Chill = int(Current_day['hourly'][i]['WindChillC'])
            Cloud_Cover_Percentage = int(Current_day['hourly'][i]['cloudcover'])
            Humidity_Percentage = int(Current_day['hourly'][i]['humidity'])
            Precipitation = float(Current_day['hourly'][i]['precipMM'])
            Pressure = float(Current_day['hourly'][i]['pressure'])
            Ambient_Temp = float(Current_day['hourly'][i]['tempC'])
            Visibility = int(Current_day['hourly'][i]['visibility'])
            Weather_Description = Current_day['hourly'][i]['weatherDesc'][0]['value']
            Wind_Direction = int(Current_day['hourly'][i]['winddirDegree'])
            Wind_Speed = int(Current_day['hourly'][i]['windspeedKmph'])
            
            all=[Sunrise_time,Sunset_time,Time,Wind_Chill,Cloud_Cover_Percentage,Humidity_Percentage,Precipitation,
             Pressure,Ambient_Temp,Visibility,Weather_Description,Wind_Direction,
             Wind_Speed]
            WMS_Data.append(all)
        
           
        WMS_Data1 = pd.DataFrame(WMS_Data,columns=('Sunrise_time','Sunset_time','Time','Wind_Chill','Cloud_Cover_Percentage',
                                                   'Humidity_Percentage','Precipitation',
                                                   'Pressure','Ambient_Temp','Visibility',
                                                   'Weather_Description','Wind_Direction',
                                                   'Wind_Speed'))
        #pdb.set_trace()
        #WMS_Data1.rename(columns = {'Unnamed: 0':'Hour'}, inplace = True)  

        self.Current_date = Current_date
        self.time = Run_time[0:2]
        WMS_Data1['Date_DD_MM_YYYY'] = pd.Series([self.Current_date for i in range(len(WMS_Data1))])
        path = cn.ExternalWMSPath+'/'+'ExternalWMS' + '_' + Current_date+'_'+Run_time[0:2]+'.csv'
        WMS_Data1.to_csv(path)
        
        return 0
    
    
    def downloadExternalGFS(self):
        
        a = str(datetime.datetime.now())[11:16]+ "th_Hour"
        latitude, longitude, tz = 23.845, 75.801, 'Asia/Kolkata'
        start = pd.Timestamp(datetime.date.today(), tz=tz)
        end = start + pd.Timedelta(days=3)
        irrad_vars = ['ghi', 'dni', 'dhi']
        model = GFS()
        data = model.get_processed_data(latitude, longitude, start, end)
        if data.isnull().values.any() == True:
            resampled_data2 = pd.read_csv('GFS.csv')
        elif a[0:5] == '23:00':
            resampled_data2 = data.resample('15min').interpolate()[108:204]
        else:
            resampled_data2 = data.resample('15min').interpolate()[12:108]
            #resampled_data2 = data.resample('15min').interpolate()[12:108]
            #resampled_data = data.resample('60min').interpolate()[3:27]
            #resampled_data1 = data.resample('10min').interpolate()[18:162]
        #resampled_data.to_csv(str(start)[0:10] +"_"+a+"_all_data_60min_"+"Barod.csv")
        #resampled_data1.to_csv(str(start)[0:10] +"_"+a+"_all_data_10min_"+"_Barod.csv")
        resampled_data2.reset_index(inplace = True)
        resampled_data2.rename(columns = {'index':'DateTime'}, inplace = True)
        resampled_data2['DateTime'] = pd.Series(str(resampled_data2.loc[i,'DateTime']).split('+')[0] for i in range(len(resampled_data2)))
        name = 'ExternalGFS.csv'
        #pdb.set_trace()
        cols = ['dhi', 'dni', 'ghi']
        for col in cols:
                resampled_data2[col] = round(resampled_data2[col],2)
        path = os.path.join(cn.ExternalWMSPath,name)
        if name not in os.listdir(cn.ExternalWMSPath):
                
            resampled_data2.drop_duplicates(inplace = True)
            resampled_data2.to_csv(path)
        else:
            df = pd.read_csv(path)
            df = df[cn.GFScols]
            df.drop_duplicates(inplace = True)
            df.reset_index(inplace = True, drop = True)
            resampled_data2 = resampled_data2[cn.GFScols]
            df = pd.concat([resampled_data2, df], axis = 0)
            df.drop_duplicates(inplace = True)
            df.sort_values(by = 'DateTime', inplace = True)
            df.reset_index(inplace = True, drop = True)
            df.to_csv(path)
            

        
        pass
    
    
    
    def saveData(self):
        save = SaveFiles()
        #save.save()
        return 0
    
    
    

    
    
    
    
    