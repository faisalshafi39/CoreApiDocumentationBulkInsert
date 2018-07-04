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
                endpointsmodelname = endpointsmodelname.split(',')
        except:
            endpointsmodelname= None        
        for value in item.getElementsByTagName('Endpoint'):           
            try:
                endpointsname = item.getElementsByTagName('Endpoint_Name')[0].firstChild.nodeValue.strip()
            except:
                endpointsname = ''
              
            cursor.execute("select id from endpoints where Name = ?",endpointsname)
            endpointid = cursor.fetchone()     
        if  isinstance(endpointsmodelname,list) :  
            print "hhhhh" ,endpointsmodelname
            for index,endpointsmodel in enumerate(endpointsmodelname):
                try:
                    if '[]' in endpointsmodel:
                        endpointsmodel=endpointsmodel.split('[]')
                        endpointsmodel = endpointsmodel[0]
                        isarray = True
                    isarray = False    
                    cursor.execute("select id from models where Name = ?",endpointsmodel)
                    modelid = cursor.fetchone() 
                    print modelid,endpointsmodel
                    # if endpointid == None and modelid == None:
                    # Parsing Request Body parameters
                    for index2,params in enumerate(item.getElementsByTagName('param')):
                        if index == index2:
                            bodyname = params.attributes['name'].value.strip()
                            cursor.execute("select * from body where Name = ? and EndPointID=? ",bodyname,endpointid[0])
                            repeatbody = cursor.fetchone() 
                            print repeatbody,"killamammama"
                            if repeatbody == None:
                                print "lalalaliijjjnnnn"
                                cursor.execute('EXEC BodyInsert @Name=?, @ModelID=?, @EndPointID=?, @Description=?, @Filter=?, @BodyType=?, @IsArrayType=?'
                                , bodyname, modelid[0],endpointid[0],None,None,'Request', isarray)
                                cnxn.commit()
                except:
                    print "hjjjnnnnn"
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
                    if 'T:BQECore.Model.IEnumerable' in returns:
                        print "babay1" 
                        returns = re.sub('T:BQECore.Model.IEnumerable', '', returns)
                        returns = re.sub('{Model.','',returns)
                        returns = re.sub('}','',returns) 
                        isarray = True  
                    elif 'T:BQECore.Model.' in returns:   
                        returns = re.sub('T:BQECore.Model.','',returns)
                    elif  'T:System.' in returns:
                        print "req"
                        returns = re.sub('T:System.','',returns) 
                    elif 'System.' in returns:
                        print "req"
                        returns = re.sub('System.','',returns)     
                    
                    isarray = False    
                    cursor.execute("select id from models where Name = ?",returns)
                    modelid = cursor.fetchone() 
                    print "kslaksalskalsk"
                    cursor.execute('EXEC BodyInsert @Name=?, @ModelID=?, @EndPointID=?, @Description=?, @Filter=?, @BodyType=?,@IsArrayType=?'
                    , responsebodyname, modelid[0],endpointid[0],None,None,'Response',isarray)

                    cnxn.commit()
                    
                except:
                    print "kikkmnnnn"
                    pass
        else:
            print "jjjjj" 
            try:
                if '[]' in endpointsmodelname:
                    endpointsmodelname=endpointsmodelname.split('[]')
                    endpointsmodelname = endpointsmodelname[0]
                    isarray = True
                isarray = False    
                cursor.execute("select id from models where Name = ?",endpointsmodelname)
                modelid = cursor.fetchone() 
                # if endpointid == None and modelid == None:
                # Parsing Request Body parameters
                bodyname = item.getElementsByTagName('param')[0].attributes['name'].value.strip()
                print bodyname
                cursor.execute("select * from body where Name = ? and EndPointID=? ",bodyname,endpointid[0])
                repeatbody = cursor.fetchone() 
                if repeatbody == None:
                    print "iklllll"
                    cursor.execute('EXEC BodyInsert @Name=?, @ModelID=?, @EndPointID=?, @Description=?, @Filter=?, @BodyType=?, @IsArrayType=?', bodyname, modelid[0],endpointid[0],None,None,'Request', isarray)
                    cnxn.commit() 
                    print "yesss" 
            except:
                print "ghh,,,,"
                pass     
            try:             
                # Parsing Response Body parameters
                print "i am in response body"
                returns = item.getElementsByTagName('returns')[0].attributes['cref'].value.strip()
                print returns
                responsebodyname = item.getElementsByTagName('returns')[0].firstChild.nodeValue.strip()
                # if re.findall('BQECore.Model.',responsebodyname) != -1:
                #     print 'a'
                #     responsebodyname = responsebodyname.split('.')
                #     responsebodyname = responsebodyname[4]
                #     responsebodyname = re.sub('(BQECore','',responsebodyname)
                #     print responsebodyname
                # else: 
                if 'T:BQECore.Model.IEnumerable' in returns:
                    print "babay"   
                    returns = re.sub('T:BQECore.Model.IEnumerable', '', returns)
                    returns = re.sub('{Model.','',returns)
                    returns = re.sub('}','',returns) 
                    isarray = True 
                elif 'T:BQECore.Model.' in returns:   
                    returns = re.sub('T:BQECore.Model.','',returns)
                elif  'T:System.' in returns:
                    print "req"
                    returns = re.sub('T:System.','',returns) 
                elif 'System.' in returns:
                    print "req"
                    returns = re.sub('System.','',returns) 
                 
                isarray = False        
                returns = re.sub('T:BQECore.Model.','',returns)
                print returns
                cursor.execute("select id from models where Name = ?",returns)
                modelid = cursor.fetchone() 
                print modelid
                cursor.execute('EXEC BodyInsert @Name=?, @ModelID=?, @EndPointID=?, @Description=?, @Filter=?, @BodyType=?,@IsArrayType=?'
                                , responsebodyname, modelid[0],endpointid[0],None,None,'Response',isarray)

                cnxn.commit()  
            except:
                print "hmmmmm"
                pass             
                
                   
    
print("Body Successfully Inserted")   
#Closing SQL SERVER Connection 
cnxn.close()



