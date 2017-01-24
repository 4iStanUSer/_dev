from pymongo import MongoClient

def forecast_db():

    connnection = MongoClient('localhost', 27017)
    forecast = connnection.forecast
    return forecast

def initialise_db():
    pass
#drop existing database

#select from database

#delete collection

#add document into collection

#get all documents

