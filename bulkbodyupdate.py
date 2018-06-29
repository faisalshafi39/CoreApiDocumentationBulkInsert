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
resultapiname = []	
verbs = ''
count = 0
api_description_bullets = ''

for item in endpointsitemlist:    
    #Parsing Api EndPoint Values        
    if 'M:' in item.attributes['name'].value:
        
        endpointsmodelname = item.attributes['name'].value.strip()
        try:
            endpointsmodelname=endpointsmodelname[endpointsmodelname.find("(")+1:endpointsmodelname.find(")")]
            
            endpointsmodelname = re.sub('BQECore.Model.','',endpointsmodelname)
            
            if endpointsmodelname.__contains__('System.'):
                endpointsmodelname = re.sub('System.','',endpointsmodelname)
        except:
            endpointsmodelname= None        

        for value in item.getElementsByTagName('Endpoint'):           
            try:
                endpointsname = item.getElementsByTagName('Endpoint_Name')[0].firstChild.nodeValue.strip()
            except:
                endpointsname = ''
              
            cursor.execute("select id from endpoints where Name = ?",endpointsname)
            endpointid = cursor.fetchone() 
        
        try:
            cursor.execute("select id from models where Name = ?",endpointsmodelname)
            modelid = cursor.fetchone() 
            # if endpointid == None and modelid == None:
            # Parsing Request Body parameters
            bodyname = item.getElementsByTagName('param')[0].attributes['name'].value.strip()
            print bodyname,modelid[0],endpointid[0],'Request'
            cursor.execute('EXEC BodyInsert @Name=?, @ModelID=?, @EndPointID=?, @Description=?, @Filter=?, @BodyType=?'
                            , bodyname, modelid[0],endpointid[0],None,None,'Request')
            cnxn.commit()  
        except:
            pass     
        try:             
            # Parsing Response Body parameters
            returns = item.getElementsByTagName('returns')[0].attributes['cref'].value.strip()
            responsebodyname = item.getElementsByTagName('returns')[0].firstChild.nodeValue.strip()
            # if re.findall('BQECore.Model.',responsebodyname) != -1:
            #     print 'a'
            #     responsebodyname = responsebodyname.split('.')
            #     responsebodyname = responsebodyname[4]
            #     responsebodyname = re.sub('(BQECore','',responsebodyname)
            #     print responsebodyname
            # else:    
            print 'b'
            returns = re.sub('T:BQECore.Model.','',returns)
            cursor.execute("select id from models where Name = ?",returns)
            modelid = cursor.fetchone() 
            print responsebodyname,modelid[0],endpointid[0],'Response'
            cursor.execute('EXEC BodyInsert @Name=?, @ModelID=?, @EndPointID=?, @Description=?, @Filter=?, @BodyType=?'
                            , responsebodyname, modelid[0],endpointid[0],None,None,'Response')

            cnxn.commit()

            
                
            
        except:
            pass    
    
print("Body Successfully Inserted")   
#Closing SQL SERVER Connection 
cnxn.close()



