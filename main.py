import os
import sys
import json
import time
from pymongo import MongoClient
from elasticsearch import Elasticsearch


def connect_to_mongodb(host, username, password, mongo_db, mongo_collection):
    # MongoDB configuration
    cluster = MongoClient(
        host=host,
        serverSelectionTimeoutMS = 3000,
        username=username,
        password=password
    )

    # connect to db
    db = cluster[mongo_db]

    # connect to collection
    collection = db[mongo_collection]

    return collection



# first load all needed environment variables
local_mongo_host = os.environ['LOCAL_MONGO_HOST'] or 'mongo_db:27017'
remote_mongo_host = os.environ['REMOTE_MONGO_HOST'] or 'team08-21.studenti.fiit.stuba.sk/mongo_db'

mongo_username = os.environ['MONGO_INITDB_ROOT_USERNAME'] or 'root'
mongo_password = os.environ['MONGO_INITDB_ROOT_PASSWORD'] or 'password'
mongo_db = os.environ['MONGO_DB'] or 'admin'
mongo_collection = os.environ['MONGO_COLLECTION'] or 'articles'
mongo_column = os.environ['MONGO_COLUMN'] or 'html' # value of this column will be taken from mongo record and indexed in elasticsearch 
num_of_articles = int(os.environ['NUMBER_OF_ARTICLES']) or 100

elastic_container_name = os.environ['ELASTIC_CONTAINER_NAME'] or 'es01'
elastic_container_port = int(os.environ['ELASTIC_CONTAINER_PORT']) or 9200
elastic_index_name = os.environ['ELASTIC_INDEX_NAME'] or 'article_index'
elastic_index_config = os.environ['ELASTIC_INDEX_CONFIG'] or 'articles_index_config.json'
elastic_field = os.environ['ELASTIC_FIELD'] or 'text' # mongo data will be indexed in this field

# time.sleep(60) # wait 60 second for MongoDB and Elasticsearch containers

print(remote_mongo_host)

# connect to remote mongo collection
remote_articles_collection = connect_to_mongodb(remote_mongo_host, mongo_username, mongo_password, mongo_db, mongo_collection)

print(remote_articles_collection)

# # connect to local mongo collection
# local_articles_collection = connect_to_mongodb(local_mongo_host, mongo_username, mongo_password, mongo_db, mongo_collection)

# # elasticsearch configuration
# es = Elasticsearch(hosts=[
#     {
#         "host": elastic_container_name,
#         "port": elastic_contianer_port
#     }
# ])

# # create index if not exists
# if not es.indices.exists(index=elastic_index_name):
#     # firstly load index configuration
#     with open(os.getcwd() + '/' + elastic_index_config) as articles_config_file:
#         configuration = json.load(articles_config_file)

#         # create index
#         res = es.indices.create(index=elastic_index_name, settings=configuration["settings"])
        
#         # make sure index was created
#         if not res['acknowledged']:
#             print('Index wasn\'t created')
#             print(res)
#             sys.exit()
#         else:
#             print('Index successfully created.')

# # get n items from collection
# cursor = remote_articles_collection.find().limit(num_of_articles)

# print('Indexing and seeding MongoDB on your local containers started.')

# # iterate through each article form remote collection and perform indexing
# for article in cursor:
#     # retrieve and convert article's id
#     item_id_string = str(article['_id'])

#     # article's html
#     article_column_value = article[mongo_column]

#     # index article's column in Elasticsearch
#     res = es.index(
#         index=elastic_index_name,
#         doc_type='_doc',
#         id=item_id_string, # document id in Elasticsearch == article id in articles collection
#         document=json.dumps(
#             {elastic_field: article_column_value}
#         )
#     )

#     # insert into local MongoDB collection
#     local_articles_collection.insert_one({"_id": item_id_string, mongo_column: article_column_value})

# print('Indexing finished.')