# Author Faisal Shafi #

# Library Import
import pyodbc 
import re

# Creating SQL SERVER Creation
cnxn = pyodbc.connect(r"Driver={SQL Server Native Client 11.0};Server=.\SQL2016;Database=CoreRestDocumentation;uid=sa;pwd=sa")
						
cursor = cnxn.cursor()
from xml.dom import minidom

# Reading the XML from File This gets altered on the basis of your xml File Path
xmldoc = minidom.parse(r'C:\Users\Faisal.Shafi\Desktop\\BQECoreApi.xml')
itemlist = xmldoc.getElementsByTagName('member')
resultapiname = ''	
for item in itemlist:
    if item.attributes['name'].value:
        
        # Parsing Api Values
        if 'T:' in item.attributes['name'].value:
            
            apiname = item.attributes['name'].value
            if apiname.startswith('T:BQECore.Api.Controllers.'):
                resultapiname = apiname
                
                apiname = re.sub('T:BQECore.Api.Controllers.', '',
                                apiname)
                apiname = re.sub('Controller', '', apiname)
                apidescription = item.getElementsByTagName('summary'
                        )[0].firstChild.nodeValue.strip()
                # Check the Api Data in Existing Database First before Entering New Data
                cursor.execute("select * from apis where Name = ?",apiname)
                apiresults = cursor.fetchone() 
                if apiresults == None:   
                    cursor.execute('EXEC ApiInsert @Name=?, @Description=?'
                                , apiname, apidescription)
                    cnxn.commit()
    
    #Parsing Api EndPoint Values         
    if 'M:' in item.attributes['name'].value:
        endpointsname = item.attributes['name'].value.strip()
        resultapiname = re.sub('T:','',resultapiname)
        if resultapiname in endpointsname:
            endpointsname = re.sub('M:'+resultapiname+'.', '',endpointsname)
            endpointsname = re.sub(r"\(.*\)", "", endpointsname)
            try:                                    
                endpointsdescription = item.getElementsByTagName('summary')[0].firstChild.nodeValue.strip()
            except:
                endpointsdescription = None   
            # Check the endpoints Data in Existing Database First before Entering New Data
            cursor.execute("select * from endpoints where Name = ?",endpointsname)
            endpointresults = cursor.fetchone() 
            if endpointresults == None:
                cursor.execute('EXEC EndPointInsert @Name=?, @Description=?, @Apiname=?'
                                , endpointsname, endpointsdescription,apiname)
                cnxn.commit()		

print("Data Successfully Inserted")   
#Closing SQL SERVER Connection 
cnxn.close()



