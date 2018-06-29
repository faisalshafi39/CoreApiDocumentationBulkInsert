# Author Faisal Shafi #

# Library Import
import pyodbc 
import re

# Creating SQL SERVER Creation
cnxn = pyodbc.connect(r"Driver={SQL Server Native Client 11.0};Server=.\SQL2016;Database=PublicApi;uid=sa;pwd=sa")
						
cursor = cnxn.cursor()
from xml.dom import minidom

# Reading the XML from File This gets altered on the basis of your xml File Path
xmldoc = minidom.parse(r'C:\Users\Faisal.Shafi\Desktop\\BQECoreModel.xml')
models = xmldoc.getElementsByTagName('member')
for item in models:
    try:
        if 'T:' in item.attributes['name'].value:
            modelname = item.attributes['name'].value 
            if modelname.startswith('T:BQECore.Model.'):
                modelresultname = modelname
                modelresultname = re.sub('T:BQECore.Model.', '',
                                modelresultname)   
                 # for testing purposes
                if not modelresultname.__contains__('.') : 
                    # Entering Model Data        
                    #Check the Model Data in Existing Database First before Entering New Data      
                    cursor.execute("select * from models where Name = ?",modelresultname)
                    modelresults = cursor.fetchone()
                    if modelresults == None:
                        print"yserses"
                        cursor.execute('EXEC ModelInsert @Name=?'
                                            , modelresultname)
                        cnxn.commit()
            else:
                modelresultname = modelname
                modelresultname = re.sub('T:', '',
                                modelresultname)     
                # Entering Model Data        
                #Check the Model Data in Existing Database First before Entering New Data      
                cursor.execute("select * from models where Name = ?",modelresultname)
                modelresults = cursor.fetchone() 
                if modelresults == None:
                    cursor.execute('EXEC ModelInsert @Name=?'
                                        , modelresultname)
                    cnxn.commit()        
        # #Entering internal Data values            
        if 'F:' in item.attributes['name'].value :
            modelpropname = item.attributes['name'].value 
            if modelpropname.find(modelresultname) != -1:
                modelpropresultname = modelpropname
                modelpropresultname = re.sub('F:'+ modelresultname+'.', '',
                                modelpropresultname)               
                # Getting ID from Parent Model
                cursor.execute("select id from models where Name = ?",modelresultname)
                modelid = cursor.fetchone() 
                #Check the Model Data in Existing Database First before Entering New Data      
                cursor.execute("select * from modeldetails where Name = ?",modelpropresultname)
                modelpropresults = cursor.fetchone() 
                try:
                    modeldescription = item.getElementsByTagName('summary'
                        )[0].firstChild.nodeValue.strip()
                except:
                    modeldescription = None        
                try:        
                    modeltype = item.getElementsByTagName('type'
                            )[0].firstChild.nodeValue.strip() 
                    cursor.execute("select id from models where Name = ?",modeltype)
                    fundtype = cursor.fetchone() 
                    fundtype = fundtype[0]
                except:
                    fundtype = None                      
                if modelpropresults == None:
                    cursor.execute('EXEC ModelDetailsInsert @ModelId = ?, @Name=?, @Description= ?,@Type=?, @AdditionalInfo=? '
                                        , modelid[0], modelpropresultname, modeldescription, fundtype,None)
                    cnxn.commit()  
        # Inserting Data into ModelDetails Table             
        if 'P:' in item.attributes['name'].value:
            modelpropname = item.attributes['name'].value            
            if modelpropname.find(modelresultname) != -1:
                modelpropresultname = modelpropname
                modelpropresultname = re.sub('P:BQECore.Model.'+ modelresultname+'.', '',
                                modelpropresultname)               
                # Getting ID from Parent Model
                cursor.execute("select id from models where Name = ?",modelresultname)
                modelid = cursor.fetchone() 
                #Check the Model Data in Existing Database First before Entering New Data      
                cursor.execute("select * from modeldetails where Name = ?",modelpropresultname)
                modelpropresults = cursor.fetchone() 
                try:
                    modeldescription = item.getElementsByTagName('summary'
                        )[0].firstChild.nodeValue.strip()
                except:
                    modeldescription = None        
                try:        
                    modeltype = item.getElementsByTagName('type'
                            )[0].firstChild.nodeValue.strip() 
                    cursor.execute("select id from models where Name = ?",modeltype)
                    fundtype2 = cursor.fetchone() 
                    fundtype2 = fundtype2[0]   
                      
                except:
                    fundtype2 = None                      
                # if modelpropresults == None:
                print ('EXEC ModelDetailsInsert @ModelId = ?, @Name=?, @Description= ?,@Type=?, @AdditionalInfo=?'
                                    , modelid[0], modelpropresultname, modeldescription, fundtype2,None)
                cursor.execute('EXEC ModelDetailsInsert @ModelId = ?, @Name=?, @Description= ?,@Type=?, @AdditionalInfo=?'
                                    , modelid[0], modelpropresultname, modeldescription, fundtype2,None)
                cnxn.commit()
    except:
        continue  
             
print("Model Data Successfully Inserted")   
#Closing SQL SERVER Connection 
cnxn.close()



