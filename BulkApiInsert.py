# Author Faisal Shafi #

# Library Import
import pyodbc 
import re

# Creating SQL SERVER Creation
cnxn = pyodbc.connect(r"Driver={SQL Server Native Client 11.0};Server=.\SQL2016;Database=PublicApi;uid=sa;pwd=sa")
						
cursor = cnxn.cursor()
from xml.dom import minidom

# Reading the XML from File This gets altered on the basis of your xml File Path
xmldoc = minidom.parse(r'C:\Users\Faisal.Shafi\Desktop\\BQECoreApi.xml')
itemlist = xmldoc.getElementsByTagName('API')
endpointsitemlist = xmldoc.getElementsByTagName('member')
print endpointsitemlist,"alalalalalalla"
resultapiname = []	
verbs = ''
count = 0
api_description_bullets = ''
for item in itemlist:   
    # Parsing Api Values      
    try:
        apiname = item.getElementsByTagName('API_Name')[0].firstChild.nodeValue.strip()
        # print apiname,"alalalaalalal"
        resultapiname.append(apiname)
        try:     
            apidescription =  item.getElementsByTagName('API_Description')[0].firstChild.nodeValue.strip()
            # Bullets entry for api description
            try:
                bullets = item.getElementsByTagName('bullet')[0].firstChild.nodeValue.strip().split('\n')
                api_description_bullets = "<ul>"
                for bullet in bullets:
                    api_description_bullets+="<li>"+bullet.strip()+"</li>"
                api_description_bullets += "</ul>"
                apidescription+=api_description_bullets   
            except:
                api_description_bullets =''   
        except: 
            apidescription = item.getElementsByTagName('API_Descripiton')[0].firstChild.nodeValue.strip() 
            try:
                bullets = item.getElementsByTagName('bullet')[0].firstChild.nodeValue.strip().split('\n')
                api_description_bullets = "<ul>"
                for bullet in bullets:
                    api_description_bullets+="<li>"+bullet.strip()+"</li>"
                api_description_bullets += "</ul>"
                apidescription+=api_description_bullets 
            except:
                api_description_bullets =''       
        #Check the Api Data in Existing Database First before Entering New Data      
        cursor.execute("select * from apis where Name = ?",apiname)
        apiresults = cursor.fetchone() 
        if apiresults == None:  
            cursor.execute('EXEC ApiInsert @Name=?, @Description=?'
                                , apiname, apidescription)
            cnxn.commit()
    except:
        pass   

for item in endpointsitemlist:    
    #Parsing Api EndPoint Values        
    if 'M:' in item.attributes['name'].value:
        endpointsapiname = item.attributes['name'].value.strip()
        endpointsapiname = re.sub('M:BQECore.Api.','',endpointsapiname)
        endpointsname = re.sub(r"\(.*\)", "", endpointsapiname)
        endpointsapiname = re.sub('Controllers.','',endpointsapiname)
        endpointsapiname = endpointsapiname.split('.')[0]
        endpointsapiname = re.sub('Controller','',endpointsapiname)
        for apis in resultapiname:
            sqlapi = apis 
            apis = re.sub(' ','',apis)
            if apis == endpointsapiname:
                if item.getElementsByTagName('Endpoint') != []:
                    for value in item.getElementsByTagName('Endpoint'):
                        
                        try:
                            endpointsname = item.getElementsByTagName('Endpoint_Name')[0].firstChild.nodeValue.strip()
                        except:
                            endpointsname = ''
                        try:        
                            endpointsdescription = item.getElementsByTagName('summary')[0].firstChild.nodeValue.strip()
                        except:
                            endpointsdescription = None    
                        try:
                            verbs =  item.getElementsByTagName('Verb')[0].firstChild.nodeValue.strip()
                        except:
                            verbs = None  
                        # Check the endpoints Data in Existing Database First before Entering New Data      
                        cursor.execute("select * from endpoints where Name = ?",endpointsname)
                        endpointresults = cursor.fetchone() 
                        if endpointresults == None:
                            cursor.execute('EXEC EndPointInsert @Name=?, @Description=?, @Apiname=?, @Verbname=?'
                                            , endpointsname, endpointsdescription,sqlapi,verbs)
                            cnxn.commit()
print("Data Successfully Inserted")   
#Closing SQL SERVER Connection 
cnxn.close()



