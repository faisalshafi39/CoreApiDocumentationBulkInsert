import json
from pprint import pprint


# Load Json into memory
with open('C:\Users\Faisal.Shafi\Desktop\\SampleResponse.Json') as f:
    
    data = json.load(f)

import pyodbc 
import re

# Creating SQL SERVER Creation
cnxn = pyodbc.connect(r"Driver={SQL Server Native Client 11.0};Server=.\SQL2016;Database=CoreRestDocumentationJuly;uid=sa;pwd=sa")
						
cursor = cnxn.cursor()


# for values in endpoints:
for endname in data:
    cursor.execute("select APIID,ID,VerbID from endpoints where Name=? ",endname['endpoint'])
    endpoints = cursor.fetchone()
   
    print endpoints
    if endpoints is not None:
        cursor.execute("Update Endpoints set RequestURI=? , SampleResponse=? where APIID=? and ID=?",endname['url'],endname['sample'],endpoints[0],endpoints[1])
        cursor.commit()

    # print values