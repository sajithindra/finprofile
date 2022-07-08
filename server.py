import re
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
client = MongoClient('mongodb://localhost:27017/')
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )

class User(BaseModel):
    mob : str
    aadhaarno: str
    panno : str
    password : str

@app.post('/adduser')
async def adduser(user : User):
    try:
        client.finprofile.user.insert_one(dict(user))
        return True
    except Exception as e:
        print("Error inserting user: ", str(e))
        return False

class FetchProfile(BaseModel):
    mob : str

@app.post('/getuserprofile')
async def getuserprofile(profile:FetchProfile):
    filter = dict(profile)
    project = {
        '_id':0,
    }
    try : 
        result =dict(client.finprofile.user.find_one(filter,project))
        return result
    except Exception as e :
        print("Error getting user profile :" + str(e))
        return False

class FetchAadhaar(BaseModel):
    aadhaarno: str

@app.post('/fetchaadhaar')
async def fetchaadhaar( addhaar : FetchAadhaar ):
    result = {
        'address': {'housename': "Housename", 'po': 'PO NAME','pin':"121212"},
        'dob': "dd/,mm/yyyy",
    }

class FetchScore(BaseModel):
    panno : str

@app.post('/fetchcibil')
async def fetchcibil( cibil : FetchScore ):
    filter= dict(cibil)
    update = { '$set': {'cibil': 625}}

    try :
        client.finprofile.user.find_one_and_update(filter,update)
        return True
    except Exception as e :
        print("Error updating cibil score"+ str(e))
        return False
    

@app.post('/fetchequifax')
async def fetchequifax(equifax : FetchScore):
    filter = dict(equifax)
    update = { '$set': {'equifax': 630}}
    try :
        client.finprofile.user.find_one_and_update(filter,update)
        return True
    except Exception as e :
        print ("Error updating equifax score :"+ str(e))
        return False

@app.post('/fetchexperian')
async def fetchexperian(experian : FetchScore ):
    filter = dict(experian)
    update = { '$set': {'experian': 635}}
    try :
        client.finprofile.user.find_one_and_update(filter,update)
        return True
    except Exception as e :
        print ("Error updating experimentian score :"+ str(e))
        return False

@app.post('/fetchcrif')
async def fetchcrif(crif : FetchScore ):
    filter = dict(crif)
    update = { '$set': {'crif':640}}
    try :
        client.finprofile.user.find_one_and_update(filter,update)
        return True
    except Exception as e :
        print ("Error updating experimentian score :"+ str(e))
        return False

@app.post('/finscore')
async def finscore(user : FetchProfile):
    filter = dict(user)
    project = {
        '_id': 0,
        'cibil':1,
        'equifax':1,
        'experian':1,
        'crif':1
    }
    try : 
        result = dict(client.finprofile.user.find_one(filter,project))
    except Exception as e :
        print ("Error fetching scores from profile : "+ str(e))
        return False
    score = (result['crif']+result['cibil']+result['equifax']+result['experian'])/4

    update = {'$set': {'finscore': score}}
    try : 
        client.finprofile.user.find_one_and_update(filter,update)
        return True
    except Exception as e :
        print ("Error insertting finscore :"+ str(e))
        return False

    
    
