filesave = '/home/sunil/Solar_main/modularize_Solar_Barod_development/Storage/filetxt.txt'
StoragePath = '/home/sunil/Solar_main/modularize_Solar_Barod_development/Storage'
LocalWMSPath = '/home/sunil/Solar_main/modularize_Solar_Barod_development/Storage/LocalWMS'
ExternalWMSPath = '/home/sunil/Solar_main/modularize_Solar_Barod_development/Storage/ExternalWMS'
MeterOnePath = '/home/sunil/Solar_main/modularize_Solar_Barod_development/Storage/MeterOne'
MeterTwoPath = '/home/sunil/Solar_main/modularize_Solar_Barod_development/Storage/MeterTwo' 
PreparedLocalWMSPath = '/home/sunil/Solar_main/modularize_Solar_Barod_development/Storage/PreProcessedData'
PreparedPowerPath  = '/home/sunil/Solar_main/modularize_Solar_Barod_development/Storage/PreProcessedData'
ExternalGFSPath = '/home/sunil/Solar_main/modularize_Solar_Barod_development/Storage/ExternalWMS'




localCols = ['Solar-Irradiation-Horizontal (Watt/m2)','Solar-Irradiation-Planer (Watt/m2)',
        'Ambient Temperature (Deg C)','PV Module Temperature (Deg C)','Power']
localWMSCols = ['Solar-Irradiation-Horizontal (Watt/m2)','Solar-Irradiation-Planer (Watt/m2)',
        'Ambient Temperature (Deg C)','PV Module Temperature (Deg C)','DateTime']

ExternalWMSCols = ['Wind_Chill','Cloud_Cover_Percentage','Humidity_Percentage','Precipitation','Pressure',
            'Ambient_Temp','Visibility','Wind_Direction','Wind_Speed','Date_DD_MM_YYYY']

powerCols = ['Power','DateTime']
GFScols = ['DateTime','ghi','dni','dhi']
Roundoffcols = ['dhi', 'dni', 'ghi']
CompleteExternalInputscols = [ 'Wind_Chill', 'Cloud_Cover_Percentage',
       'Humidity_Percentage', 'Precipitation', 'Pressure', 'Ambient_Temp',
       'Visibility', 'Wind_Direction', 'Wind_Speed', 'ghi', 'dni', 'dhi']




target = 'Power'


ActualInpExternal = ['Solar-Irradiation-Planer (Watt/m2)', 'Wind_Chill',
       'Cloud_Cover_Percentage', 'Humidity_Percentage', 'Precipitation',
       'Pressure', 'Ambient_Temp', 'Visibility', 'Wind_Direction',
       'Wind_Speed']


location1TemplateFilepath = '/home/sunil/Solar_main/modularize_Solar_Barod_development/templates/Location1_template.xlsx'
location2TemplateFilepath = '/home/sunil/Solar_main/modularize_Solar_Barod_development/templates/Location2_template.xlsx'


saveResultsPath = '/home/sunil/Solar_main/modularize_Solar_Barod_development/Results'
saveResultsPathForExternal = '/home/sunil/Solar_main/modularize_Solar_Barod_development/ResultsExternal'


ftpAddress = "42.104.76.156"
ftplogin = "mbcs_ftp"
ftppasswd = "Ayan#79d"