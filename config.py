import os
from flask import Flask
from pymongo import MongoClient

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\nr\x81\xf1\x172u\xa7\xcbu\xff\x85\x9cO%\xea'
    
CONNECTION_STRING = "mongodb+srv://aptswati:strawberry@cluster0.2fqdn.mongodb.net/<dbname>?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')

 
                   
