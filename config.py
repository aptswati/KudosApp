import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\nr\x81\xf1\x172u\xa7\xcbu\xff\x85\x9cO%\xea'

client = MongoClient('mongodb://datastore:27017/Kudos_db')
db = client.Kudos_db
 
                   
