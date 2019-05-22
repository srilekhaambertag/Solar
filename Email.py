import pandas as pd
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from datetime import datetime, timedelta
import os
import pdb

class Email:
    def __init__(self):
        pass
    
    
    def email(self, Reqddatetime = None, loc = 'Barod_Location1_'):
        
        fromaddr = "heliot.fns@gmail.com"
        toaddr = ['ashvin@ambertag.com','srilekha@ambertag.com']
        #toaddr = ['ashvin@ambertag.com','srilekha@ambertag.com','panchalsubhash.eee@gmail.com','sandeep.samavistenergy@gmail.com','abhinav.ag@mbcontrol.com','ashoksharma@uflexltd.com']
        delay = 0
        time = datetime.now()
        # instance of MIMEMultipart 
        msg = MIMEMultipart() 
          
        # storing the senders email address   
        msg['From'] = fromaddr 
          
        # storing the receivers email address  
        msg['To'] = ", ".join(toaddr)
        fileTime = Reqddatetime
        fileTime = fileTime.replace("-","_")
        fileTime = fileTime.replace(" ","_")
        fileTime = fileTime.replace(":","_")
        filename = loc+fileTime+".xlsx"  
        #pdb.set_trace()
        # storing the subject  
        msg['Subject'] = filename
        
        # string to store the body of the mail 
        #prediction_date = str(time.date())
        #timetoprint = str(time-timedelta(minutes =delay))[11:16]
        prediction_date = Reqddatetime[0:10]
        timetoprint = Reqddatetime[11:16]
        
        
        revision = {'05:00':'1','06:30':'2','08:00':'3','09:30':'4','11:00':'5',
                            '12:30':'6','14:00':'7','15:30':'8','17:00':'9','18:30':'10'}
                
        revisionNum = revision.get(timetoprint)
        #body = 'Dear Sir, \nPlease find attached the revised generation schedule for the 10.0 MW solar capacity connected to at SAMAVIST S/S. \nSend Date : "+prediction_date+"\nSend Time : "+timetoprint+"Hrs \nRevision No :"+ str(Revision_num) +"\nEffective From = "+str(datetime.datetime.now() + datetime.timedelta(minutes = 15))[11:16]+"Hrs\n\n\n\nWith Regards, \nTeam Heliot.'
        
        if loc == 'Barod_Location1_':
            Location = 1
        else:
            Location = 2
            
        body = 'Dear Sir, \nPlease find  attached the revised generation schedule for the 10.0 MW solar capacity connected to the Barod_location: '+str(Location)+ 'S/S.' '\nSend Date : '+prediction_date+'\nSend Time : '+timetoprint+'Hrs \nRevision No :'+ str(revisionNum) +'\nEffective From = '+str(pd.to_datetime(Reqddatetime)+timedelta(minutes =15))[11:16]+'Hrs\n\n\n\nWith Regards, \nTeam Heliot.'
                
        #pdb.set_trace()
        # attach the body with the msg instance 
        msg.attach(MIMEText(body, 'plain')) 
          
        # open the file to be sent  
        #filename = "File_name_with_extension"
        
        
        
        
        #filename = "SAMAVIST_ENERGY_33KV_2019_03_08_11_03.xlsx"
        filepath = "/home/sunil/Solar_main/modularize_Solar_Barod_development/ResultsExternal"
        finalFilePath = os.path.join(filepath,filename)
        attachment = open(finalFilePath, "rb") 
          
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
          
        # To change the payload into encoded form 
        p.set_payload((attachment).read()) 
          
        # encode into base64 
        encoders.encode_base64(p) 
           
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
          
        # attach the instance 'p' to instance 'msg' 
        msg.attach(p) 
          
        # creates SMTP session 
        s = smtplib.SMTP('smtp.gmail.com', 587) 
          
        # start TLS for security 
        s.starttls() 
          
        # Authentication 
        s.login(fromaddr, 'gmxldtejnmnyilgt') 
          
        # Converts the Multipart msg into a string 
        text = msg.as_string() 
          
        # sending the mail 
        s.sendmail(fromaddr, toaddr, text) 
          
        # terminating the session 
        s.quit() 