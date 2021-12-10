import os
import sys
import json
import time
from pymongo import MongoClient
from elasticsearch import Elasticsearch

time.sleep(60) # wait 60 second for MongoDB and Elasticsearch containers

# mongo db configuration
cluster = MongoClient(
    host='mongo_db:27017',
    serverSelectionTimeoutMS = 3000,
    username=os.environ['MONGO_INITDB_ROOT_USERNAME'] or 'root',
    password=os.environ['MONGO_INITDB_ROOT_PASSWORD'] or 'password'
)

# connect to admin DB in Mongo
db = cluster['admin']

# connect to 'articles' collection, MongoDB will create one if it doesn't exists
articles_collection = db['articles']

# elasticsearch configuration
# HOST="http://es01", PORT=9200
es = Elasticsearch(hosts=[
    {"host":'es01'}
])

# create index if not exists
if not es.indices.exists(index='articles_index'):
    # firstly load index configuration
    with open(os.getcwd() + '/articles_index_config.json') as articles_config_file:
        configuration = json.load(articles_config_file)

        # create index
        res = es.indices.create(index="articles_index", settings=configuration["settings"])
        
        # make sure index was created
        if not res['acknowledged']:
            print('Index wasn\'t created')
            print(res)
            sys.exit()
        else:
            print('Index successfully created.')

# get all items from articles collection
cursor = articles_collection.find()

print('Indexing started.')

# iterate through each article form articles collection and perform indexing
for article in cursor:
    # retrieve and convert article's id
    item_id_string = str(article['_id'])
    # index article's html in Elasticsearch
    res = es.index(
        index='articles_index',
        doc_type='_doc',
        id=item_id_string, # document id in Elasticsearch == article id in articles collection
        document=json.dumps(
            {"text": article['html']}
        )
    )

print('Indexing finished.')