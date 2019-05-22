
from ftplib import FTP
import os
import fileinput
import smtplib
import pandas as pd
import datetime
from datetime import timedelta
class FTP:
    def __init__(self):
        pass
    
    def ftp(self, Reqddatetime = None, loc = 'Barod_Location1_'):
        #Time = datetime.datetime.now()
        #Time = datetime.datetime(2019,3,6,11,34)
        #Prediction_Date0 = pd.Timestamp(datetime.date.today())
        #Prediction_Date = str(pd.to_datetime(Prediction_Date0).date())
        #
        ftp = FTP()
        ftp.set_debuglevel(2)
        #ftp.connect('43.252.251.83', 21)
        ftp.connect('111.118.215.222', 21)
        
        ftp.login('amber_tag@mbscada.com','ocT8H-p,iib3')
        if loc == 'Barod_Location1_':
            ftp.cwd('/todcln_s1/')
        else:
            ftp.cwd('/todcln_s2/')
            
        #filename ='2019_02_27_15_43.csv'
        #time = str(Time - timedelta(minutes = 5))[11:16]
        #filename = 'REFEX_ENERGY_33KV_'+str(Prediction_Date.replace('-', '_'))+'_'+str(time.replace(':','_'))+'.xlsx'
        #filename = 'Prediction1.xlsx'
        fileTime = Reqddatetime
        fileTime = fileTime.replace("-","_")
        fileTime = fileTime.replace(" ","_")
        fileTime = fileTime.replace(":","_")
        filename = loc+fileTime+".xlsx" 
        filepath = os.path.join('/home/sunil/Solar_main/Solar/modularize_Solar_Barod/Results',filename)
        
        fp = open(filepath,'rb')
        ftp.storbinary('STOR %s' % os.path.basename(filepath), fp, 1024)
        #os.chdir('/home/sunil/Active_Power/Mails')
        
        fp.close()