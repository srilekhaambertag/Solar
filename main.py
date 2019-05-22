from DataAcquisition import DataAcquisition
from DataPreparation import DataPreparation
from DataModelling import DataModelling
from Email import Email
from FTP import FTP
import numpy as np
import pandas as pd
import os
import glob
import Config as cn
import time
import pdb 

dA = DataAcquisition()
'''dA.saveData()
dA.downloadlocalWMS()
dA.downloadPowerMeterOne()
dA.downloadPowerMeterTwo()'''
dP = DataPreparation()
CurrentExternaWMSData = dP.prepareExternalWeather( date = dA.Current_date, time = dA.time)
dP.interpolateExternalWMS(df = CurrentExternaWMSData.copy())

dM = DataModelling()
dM.buildLocalModel(dM.localDfMeterone)
dM.buildLocalModel(dM.localDfMetertwo,meter = 'two')

dM.readLocalDNI_externalWMS(dP.interpolatedWeatData)
dM.buildExternalModel(state = None)
dM.buildExternalModel(meter = 'two',state = None)



mergedDf = dM.readInputData()
ypredMeterOne, ypredMeterTwo = dM.forecast(mergedDf)


dM.readExternalWMSGFS(df = dP.ExternalWMSGFSData)
dM.buildExternalWMSGFSModel(df = dM.ExtData.drop(['DateTime','Unnamed: 0'], axis = 1))
dM.readExternalWMSGFS(df = dP.ExternalWMSGFSData, meter = 'two')
dM.buildExternalWMSGFSModel(df = dM.ExtData.drop(['DateTime','Unnamed: 0'],axis = 1), meter = 'two')

mergedDfCompleteExtInps = dM.readForecatedInputData()
dM.ForecastUsingExternalWMSGFS(mergedDfCompleteExtInps[cn.CompleteExternalInputscols])
dM.ForecastUsingExternalWMSGFS(mergedDfCompleteExtInps[cn.CompleteExternalInputscols], meter = 'two')




em = Email()
#pdb.set_trace()
em.email(Reqddatetime = dM.DateTime)
em.email(Reqddatetime = dM.DateTime,loc = 'Barod_Location2_')



'''ft = FTP()
ft.ftp(Reqddatetime = dM.DateTime)
ft.ftp(Reqddatetime = dM.DateTime,loc = 'Barod_Location2_')'''

#dM.ExtdataMeterOne['DateTime']



    

