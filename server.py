from cmath import e
from inspect import modulesbyfile
from pydoc import cli
import re
from xmlrpc import client
from click import password_option
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from pyrsistent import T
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

class FecthProfile(BaseModel):
    mob : str

@app.post('/getuserprofile')
async def getuserprofile(profile:FecthProfile):
    filter = dict(profile)
    project = {
        '_id':0,
    }
    try : 
        result =dict(client.finprofile.user.find_one(filter =filter,project =project))
        return result
    except Exception as e :
        print("Error getting user profile :" + str(e))
        return False
    