import pandas as pd
import numpy as np
import glob
import os 
import pickle
import Config as cn
import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from SaveFiles import SaveFiles
import pdb

class DataModelling:
    def __init__(self):
        self.localDfMeterone,self.localDfMetertwo  = self.readLocalData()
    
    def buildLocalModel(self, df, meter = 'one'):
        X = df.drop(cn.target, axis = 1)
        y = df[cn.target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                            test_size=0.2, random_state=42)
        
        regr = RandomForestRegressor(max_depth=2, random_state=0,n_estimators=10)
        regr.fit(X_train,y_train)
        y = regr.predict(X_test)
        
        try:
            
            localmodelPath = os.path.join(cn.StoragePath,'localWMSModel')
            os.makedirs(localmodelPath)

        except:
            pass
        
        if meter == 'one':
            self.printoutError(y, y_test.values)
            name = str(datetime.datetime.now())[0:16] +'_finalized_localWMSmodel_meterone.sav' 
            filename = os.path.join(localmodelPath,name)
        else:
            self.printoutError(y, y_test.values, meter = 'two')
            name = str(datetime.datetime.now())[0:16] +'_finalized_localWMSmodel_metertwo.sav' 
            filename = os.path.join(localmodelPath,name)
            
        pickle.dump(regr, open(filename, 'wb'))
        return 0
    
    def readLocalData(self):
        self.localwmsPath = os.path.join(cn.PreparedLocalWMSPath,'UpdatedLocalWMS.xlsx')
        self.powerMeterOne = os.path.join(cn.PreparedPowerPath,'meterOne.csv')
        self.powerMeterTwo = os.path.join(cn.PreparedPowerPath,'meterTwo.csv')
        
        self.localWeatData = pd.read_excel(self.localwmsPath)
        self.meterOnedata = pd.read_csv(self.powerMeterOne)
        self.meterTwodata = pd.read_csv(self.powerMeterTwo)
        self.meterOnedata = self.meterOnedata[cn.powerCols]
        self.meterTwodata = self.meterTwodata[cn.powerCols]
        self.localWeatData.drop_duplicates(inplace = True)
        self.meterOnedata.drop_duplicates(inplace = True)
        self.meterTwodata.drop_duplicates(inplace = True)
        
        self.meterOnedata['DateTime'] = pd.to_datetime(self.meterOnedata['DateTime'])
        self.meterTwodata['DateTime'] = pd.to_datetime(self.meterTwodata['DateTime'])
        dfmeterone = pd.merge(self.localWeatData, self.meterOnedata, left_on = 'DateTime', right_on = 'DateTime',
                      how = 'inner')
        dfmeterone = dfmeterone[cn.localCols]
        dfmetertwo = pd.merge(self.localWeatData, self.meterTwodata, left_on = 'DateTime', right_on = 'DateTime',
                      how = 'inner')
        dfmetertwo = dfmetertwo[cn.localCols]
        return dfmeterone,dfmetertwo
    
    
    def readLocalDNI_externalWMS(self, extWeaData = None):
        #weaDniData =  pd.
        cols = ['Solar-Irradiation-Planer (Watt/m2)','DateTime']
        localDNIdf = self.localWeatData[cols]
        self.ExtWMSLocalDniData = pd.merge(localDNIdf,extWeaData, left_on = 'DateTime', right_on = 'DateTime',
                                      how = 'inner')
        self.ExtdataMeterOne = pd.merge(self.ExtWMSLocalDniData, self.meterOnedata, left_on = 'DateTime', right_on = 'DateTime',
                      how = 'inner')
        self.ExtdataMeterOne.drop_duplicates(inplace = True)
        self.ExtdataMeterTwo = pd.merge(self.ExtWMSLocalDniData, self.meterTwodata, left_on = 'DateTime', right_on = 'DateTime',
                      how = 'inner')
        self.ExtdataMeterTwo.drop_duplicates(inplace = True)
        
    def buildExternalModel(self, meter = 'one', state = 42):
        
        if meter =='one':
            tempDf = self.ExtdataMeterOne.copy()
            tempDf.drop('DateTime', inplace = True, axis = 1)
            X = tempDf.drop(cn.target, axis = 1)
            #pdb.set_trace()
            y = tempDf[cn.target]
        else:
            tempDf = self.ExtdataMeterTwo.copy()
            tempDf.drop('DateTime', inplace = True, axis = 1)
            X = tempDf.drop(cn.target, axis = 1)
            y = tempDf[cn.target]
          
        X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                            test_size=0.2, random_state=state)
        #pdb.set_trace()  
        regr = RandomForestRegressor(max_depth=20, random_state=0,n_estimators=100)
        regr.fit(X_train,y_train)
        y = regr.predict(X_test)
        

        try:
            externalmodelPath = os.path.join(cn.StoragePath,'ExternalWMSModel')
            os.makedirs(externalmodelPath)

        except:
            pass
        
        if meter == 'one':
            self.printoutError( y, y_test.values,use = 'External')
            name = str(datetime.datetime.now())[0:16] +'_finalized_externalWMSmodel_meterone.sav' 
            filename = os.path.join(externalmodelPath,name)
            self.RFmeterOnemodel = regr
            # Forecast for the next future points using regr model
        else:
            self.printoutError( y, y_test.values,use = 'External', meter = 'two')
            name = str(datetime.datetime.now())[0:16] +'_finalized_externalWMSmodel_metertwo.sav' 
            filename = os.path.join(externalmodelPath,name)
            self.RFmeterTwomodel = regr
            # Forecast for the next future points using regr model
            
        pickle.dump(regr, open(filename, 'wb'))
    
    def printoutError(self, ypred = None, ytest = None, use = 'local', meter = 'one'):
        df = pd.concat([pd.Series(ypred),pd.Series(ytest)], axis = 1)
        df.rename(columns = {0:'forecasted', 1:'actuals'}, inplace = True)
        
        df = df[df['actuals']>0]
        df ['error'] = (abs(df['actuals']-df['forecasted'])/10000)*100
        print('The errors using {} for meter {} is {}'.format(use, meter, sum(df['error']>15)/len(df)))
        
        pass
    
    

        
    def readInputData(self):
        # Do the following for meter 1 and meter 2: 
        # Read the future inputs
        # Load saved model for RandomForest or pass from the newly trained model using external WMS and local DNI model
        # Forecast ypred for the future points
        # Save outputs im required template 
        
        ########## Reading forecasting External and GFS data ############
        #interpolatedWeatData = pd.read_csv('/home/ashvin/Desktop/Solar/modularize_Solar_Barod/Storage/PreProcessedData/interpolatedExternalWMS.csv')
        #ExternalGFSdata = pd.read_csv('/home/ashvin/Desktop/Solar/modularize_Solar_Barod/Storage/ExternalWMS/ExternalGFS.csv')
        
        interpolatedWMSPath = os.path.join(cn.PreparedLocalWMSPath,'interpolatedExternalWMS.csv')
        ExternalGFSdataPath = os.path.join(cn.ExternalWMSPath,'ExternalGFS.csv')
        interpolatedWeatData = pd.read_csv(interpolatedWMSPath)
        ExternalGFSdata = pd.read_csv(ExternalGFSdataPath)
        interpolatedWeatData['DateTime'] = pd.to_datetime(interpolatedWeatData['DateTime'])
        ExternalGFSdata['DateTime'] = pd.to_datetime(ExternalGFSdata['DateTime'])
        currentDate  = datetime.datetime.now()
        interpolatedWeatData['Date'] = pd.Series(interpolatedWeatData.loc[i,'DateTime'].date() for i in range(len(interpolatedWeatData)))
        ExtWMSdata = interpolatedWeatData[interpolatedWeatData['Date'] ==currentDate.date()]
        ExternalGFSdata['Date'] = pd.Series(ExternalGFSdata.loc[i,'DateTime'].date() for i in range(len(ExternalGFSdata)))
        ExtGFSdata = ExternalGFSdata[ExternalGFSdata['Date'] ==currentDate.date()]
        mergedDf = pd.merge(ExtWMSdata,ExtGFSdata, left_on = 'DateTime', right_on = 'DateTime', how = 'inner')
        mergedDf.rename(columns = {'dni':'Solar-Irradiation-Planer (Watt/m2)'}, inplace = True)
        mergedDf['Time'] = pd.Series(mergedDf.loc[i,'DateTime'].time() for i in range(len(mergedDf)))
        mergedDf = mergedDf[mergedDf['Time']>= currentDate.time()]
        #mergedDf = mergedDf[mergedDf['Time']>= datetime.time(12, 00, 35, 231725)]
        mergedDf.reset_index(inplace = True, drop = True)
        mergedDf.drop_duplicates(['DateTime'], inplace = True)
        return mergedDf
    
    
    def forecast(self, df):
        ypredMeterOne = self.RFmeterOnemodel.predict(df[cn.ActualInpExternal])
        ypredMeterTwo = self.RFmeterTwomodel.predict(df[cn.ActualInpExternal])
        save  =SaveFiles()
        save.saveForecastedPower(df,ypredMeterOne)
        save.saveForecastedPower(df,ypredMeterTwo,loc = '/Barod_Location2_')
        self.DateTime = save.datetime
        return ypredMeterOne,ypredMeterTwo
    
    
    
    
    
    def readExternalWMSGFS(self, df = None, meter = 'one'):
        # This is to read the complete external data with power for
        #preparing data for train and testing data sets in buildExternalWMSGFSModel
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        self.meterOnedata['DateTime'] = pd.to_datetime(self.meterOnedata['DateTime'])
        
        if meter == 'one':
            self.ExtData = pd.merge(df, self.meterOnedata, left_on = 'DateTime', right_on = 'DateTime',
                          how = 'inner')
        else:
            self.ExtData = pd.merge(df, self.meterTwodata, left_on = 'DateTime', right_on = 'DateTime',
                               how = 'inner')
            
        self.ExtData.drop_duplicates(inplace = True)    
            
        pass
    
    
    def buildExternalWMSGFSModel(self, df = None, meter = 'one'):
        X = df.drop(cn.target, axis = 1)
        #pdb.set_trace()
        y= df[cn.target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                            test_size=0.2, random_state=42)
        #pdb.set_trace()
        if meter == 'one':
            self.modelRFExternalmeterOne = RandomForestRegressor(max_depth=20, random_state=0,n_estimators=100)
            self.modelRFExternalmeterOne.fit(X_train,y_train)
            y = self.modelRFExternalmeterOne.predict(X_test)
        else: 
            self.modelRFExternalmeterTwo = RandomForestRegressor(max_depth=20, random_state=0,n_estimators=100)
            self.modelRFExternalmeterTwo.fit(X_train,y_train)
            y = self.modelRFExternalmeterTwo.predict(X_test)
        
        self.printoutExternalError(y, y_test.values, met = meter )
        print(y)
        print(y_test.values)
        pass
    
    def printoutExternalError(self, ypred = None, ytest = None, met = None):
        df = pd.concat([pd.Series(ypred),pd.Series(ytest)], axis = 1)
        df.rename(columns = {0:'forecasted', 1:'actuals'}, inplace = True)
        
        df = df[df['actuals']>0]
        df ['error'] = (abs(df['actuals']-df['forecasted'])/10000)*100
        print('The errors for meter {} is {}'.format( met, sum(df['error']>15)/len(df)))
        
        pass
    
    def readForecatedInputData(self):
        # Do the following for meter 1 and meter 2: 
        # Read the future inputs
        # Load saved model for RandomForest or pass from the newly trained model using external WMS and local DNI model
        # Forecast ypred for the future points
        # Save outputs im required template 
        
        ########## Reading forecasting External and GFS data ############
        #interpolatedWeatData = pd.read_csv('/home/ashvin/Desktop/Solar/modularize_Solar_Barod/Storage/PreProcessedData/interpolatedExternalWMS.csv')
        #ExternalGFSdata = pd.read_csv('/home/ashvin/Desktop/Solar/modularize_Solar_Barod/Storage/ExternalWMS/ExternalGFS.csv')
        
        interpolatedWMSPath = os.path.join(cn.PreparedLocalWMSPath,'interpolatedExternalWMS.csv')
        ExternalGFSdataPath = os.path.join(cn.ExternalWMSPath,'ExternalGFS.csv')
        interpolatedWeatData = pd.read_csv(interpolatedWMSPath)
        ExternalGFSdata = pd.read_csv(ExternalGFSdataPath)
        interpolatedWeatData['DateTime'] = pd.to_datetime(interpolatedWeatData['DateTime'])
        ExternalGFSdata['DateTime'] = pd.to_datetime(ExternalGFSdata['DateTime'])
        currentDate  = datetime.datetime.now()
        interpolatedWeatData['Date'] = pd.Series(interpolatedWeatData.loc[i,'DateTime'].date() for i in range(len(interpolatedWeatData)))
        ExtWMSdata = interpolatedWeatData[interpolatedWeatData['Date'] ==currentDate.date()]
        ExternalGFSdata['Date'] = pd.Series(ExternalGFSdata.loc[i,'DateTime'].date() for i in range(len(ExternalGFSdata)))
        ExtGFSdata = ExternalGFSdata[ExternalGFSdata['Date'] ==currentDate.date()]
        mergedDf = pd.merge(ExtWMSdata,ExtGFSdata, left_on = 'DateTime', right_on = 'DateTime', how = 'inner')
        #mergedDf.rename(columns = {'dni':'Solar-Irradiation-Planer (Watt/m2)'}, inplace = True)
        mergedDf['Time'] = pd.Series(mergedDf.loc[i,'DateTime'].time() for i in range(len(mergedDf)))
        mergedDf = mergedDf[mergedDf['Time']>= currentDate.time()]
        #mergedDf = mergedDf[mergedDf['Time']>= datetime.time(12, 00, 35, 231725)]
        mergedDf.reset_index(inplace = True, drop = True)
        mergedDf.drop_duplicates(['DateTime'], inplace = True)
        self.mergedDfCompleteExtInps = mergedDf
        return mergedDf
    
    
    def ForecastUsingExternalWMSGFS(self, df = None, meter = 'one'):
        save  =SaveFiles()
        if meter == 'one':
            self.ExtPowerMeterOne = pd.DataFrame()
            ypredOne = self.modelRFExternalmeterOne.predict(df)
            self.ExtPowerMeterOne = pd.concat([pd.Series(self.mergedDfCompleteExtInps['DateTime'].values),pd.Series(ypredOne)], axis = 1)
            self.ExtPowerMeterOne.rename(columns = {1:'Forecasted', 0:'DateTime'}, inplace = True)
            save.saveForecastedPowerFromExternalInps(self.ExtPowerMeterOne)
        else:    
            self.ExtPowerMeterTwo = pd.DataFrame()
            ypredTwo = self.modelRFExternalmeterTwo.predict(df)
            self.ExtPowerMeterTwo = pd.concat([pd.Series(self.mergedDfCompleteExtInps['DateTime'].values),pd.Series(ypredTwo)], axis = 1)
            self.ExtPowerMeterTwo.rename(columns = {1:'Forecasted', 0:'DateTime'}, inplace = True)
            save.saveForecastedPowerFromExternalInps(self.ExtPowerMeterTwo,loc = '/Barod_Location2_')
        pass