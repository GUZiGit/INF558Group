import pymongo

myClient = pymongo.MongoClient('mongodb://54.193.51.217')

crawlerDB = myClient['crawler']
usc = crawlerDB['USC']

content = {'url':'aurl','content':'a html content ', 'title':'a title'}

usc.insert_one(content)


