from pymongo import MongoClient


def connector():
    """
    Return

    :return:
    :rtype:
    """
    connnection = MongoClient('localhost', 27017)

    forecast = connnection.forecast
    return forecast


#drop existing database

#select from database

#delete collection

#add document into collection

#get all documents
