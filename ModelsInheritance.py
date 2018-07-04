            
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
# Getting inherit property tags
for item in endpointsitemlist:    
    #Parsing Api Inherit Values 
    if 'T:' in  item.attributes['name'].value: 
        try: 
            endpointsmodelname = item.getElementsByTagName('API_Name')[0].firstChild.nodeValue.strip() 
            cursor.execute("select id from models where Name = ?",endpointsmodelname)
            endpointsmodelID = cursor.fetchone()
        except:
            endpointsmodelname  = None  
        #Getting which is using inherited models ID\
        
    if 'M:' in item.attributes['name'].value:
            if item.getElementsByTagName('Inherits'):
                modelcontent = item.getElementsByTagName('Inherits')[0].firstChild.nodeValue.strip().split(',')
                for content in modelcontent:
                    # Getting inherited models ID
                    cursor.execute("select id from models where Name = ?",content)
                    inheritedmodelid=cursor.fetchone()
                    
                    # Checking Previously entered entries in model
                    cursor.execute("select * from InheritedModels where InheritedFrom = ?",inheritedmodelid)
                    inheritedmodeluniqueid=cursor.fetchone()
                    if inheritedmodeluniqueid == None:
                        cursor.execute('EXEC InheritedModelsInsert @InheritedFrom = ?, @ModelID=? '
                                                    , inheritedmodelid[0], endpointsmodelID[0])
                        cnxn.commit()
                                                      
            
print "Model Mapping Successfully Inserted"
#Closing SQL SERVER Connection 
cnxn.close()            