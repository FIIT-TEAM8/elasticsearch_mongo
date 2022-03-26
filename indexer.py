import os
import json
import time
from pymongo import MongoClient
from elasticsearch import Elasticsearch
import indexer_settings as settings

time.sleep(settings.indexer_wait_seconds) # wait n seconds for MongoDB and Elasticsearch containers

# connect to local MongoDB container
remote_mongo = MongoClient(settings.REMOTE_MONGO_CONN_STRING)
local_mongo = MongoClient(settings.LOCAL_MONGO_CONN_STRING)
remote_db = remote_mongo[settings.remote_mongo_database]
local_db = local_mongo[settings.remote_mongo_database]
remote_articles_collection = remote_db[settings.remote_mongo_collection]
local_collection = local_db[settings.remote_mongo_collection]
local_es = Elasticsearch("http://" + settings.local_elastic_host + ":" + settings.local_elastic_port, max_retries=10, retry_on_timeout=True)

# waiting for elastic
while not local_es.ping():
    time.sleep(10)

# retrieve articles from remote MongoDB for seeding local MongoDB container and indexing in local Elasticsearch container
cursor = remote_articles_collection.find().limit(settings.indexer_number_of_articles)
print('Articles was successfully retrieved from remote MongoDB.')

# elasticsearch configuration
# this will connect to local Elasticsearch container


# create index if not exists
if not local_es.indices.exists(index=settings.elastic_collection):
    # firstly load index configuration
    with open(os.getcwd() + '/' + "articles_index_config.json") as articles_config_file:
        configuration = json.load(articles_config_file)
        # create index
        res = local_es.indices.create(index=settings.elastic_collection, settings=configuration["settings"])
        # make sure index was created
        if not res['acknowledged']:
            print('Index wasn\'t created')
            print(res)
            exit(1)
        else:
            print('Index successfully created.')


print('Indexing in Elasticsearch and seeding MongoDB on your local containers...')

# iterate through each article form remote collection and perform indexing
cursor.rewind()
for article in cursor:
    local_collection.insert_one(article)
    article_id = str(article['_id'])
    article.pop("_id", None)
    local_es.index(index=settings.elastic_collection, id=article_id, document=json.dumps(article))

print('Indexing finished.')