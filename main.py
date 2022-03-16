import os
import sys
import json
import time
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from ssh_pymongo import MongoSession

# first load all needed environment variables
ssh_port = int(os.environ['SSH_PORT']) or 22
ssh_user = os.environ['SSH_USER'] or 'root'
ssh_password = os.environ['SSH_PASSWORD'] or 'password'
remote_ip = os.environ['REMOTE_IP'] or 'team08-21.studenti.fiit.stuba.sk'

local_mongo_uri = os.environ['LOCAL_MONGO_URI'] or 'mongodb://mongo_db'
remote_mongo_uri = os.environ['REMOTE_MONGO_URI'] or 'mongodb://localhost:27017'

mongo_username = os.environ['MONGO_INITDB_ROOT_USERNAME'] or 'root'
mongo_password = os.environ['MONGO_INITDB_ROOT_PASSWORD'] or 'password'
mongo_db = os.environ['MONGO_DB'] or 'admin'
mongo_collection = os.environ['MONGO_COLLECTION'] or 'articles'
mongo_collection_crimemaps = os.environ['MONGO_COLLECTION_CRIMEMAPS'] or 'crimemaps'
mongo_column = os.environ['MONGO_COLUMN'] or 'html' # value of this column will be taken from mongo record and indexed in elasticsearch
num_of_articles = int(os.environ['NUMBER_OF_ARTICLES']) or 100

elastic_container_name = os.environ['ELASTIC_CONTAINER_NAME'] or 'es01'
elastic_container_port = int(os.environ['ELASTIC_CONTAINER_PORT']) or 9200
elastic_index_name = os.environ['ELASTIC_INDEX_NAME'] or 'article_index'
elastic_index_config = os.environ['ELASTIC_INDEX_CONFIG'] or 'articles_index_config.json'
elastic_field = os.environ['ELASTIC_FIELD'] or 'text' # mongo data will be indexed in this field

wait_seconds = int(os.environ['WAIT_SECONDS']) or 60

time.sleep(wait_seconds) # wait n seconds for MongoDB and Elasticsearch containers

# ssh tunel on remote MongoDB on our machine
session = MongoSession(remote_ip,
    port=ssh_port,
    user=ssh_user,
    password=ssh_password,
    uri=remote_mongo_uri
)

print('Successfully connected to remote MongoDB.')

# connect to local MongoDB container
cluster = MongoClient(
    host=local_mongo_uri,
    serverSelectionTimeoutMS = 3000,
    username=mongo_username,
    password=mongo_password
)

print('Successfully connected to local MongoDB container.')

# on remote MongoDB select database, which you want to use
db = session.connection[mongo_db]

# perform authentication for remote MongoDB before using selected database
db.authenticate(mongo_username, mongo_password)

print('Successfully authenticate to access remote MongoDB selected database.')

# connect to collection on remote MongoDB
articles_collection = db[mongo_collection]

print('Retrieving articles from remote MongoDB...')

# retrieve articles from remote MongoDB for seeding local MongoDB container and indexing in local Elasticsearch container
cursor = articles_collection.find().limit(num_of_articles)
links = []



print('Articles was successfully retrieved from remote MongoDB.')

# elasticsearch configuration
# this will connect to local Elasticsearch container
es = Elasticsearch(hosts=[
    {
        "host": elastic_container_name,
        "port": elastic_container_port
    }
])

print('Successfully connected to local Elasticsearch container.')

# create index if not exists
if not es.indices.exists(index=elastic_index_name):
    # firstly load index configuration
    with open(os.getcwd() + '/' + elastic_index_config) as articles_config_file:
        configuration = json.load(articles_config_file)

        # create index
        res = es.indices.create(index=elastic_index_name, settings=configuration["settings"])

        # make sure index was created
        if not res['acknowledged']:
            print('Index wasn\'t created')
            print(res)
            sys.exit()
        else:
            print('Index successfully created.')

local_db = cluster[mongo_db]

local_collection = local_db[mongo_collection]


print('Indexing in Elasticsearch and seeding MongoDB on your local containers...')

# iterate through each article form remote collection and perform indexing
for article in cursor:
    # retrieve and convert article's id
    item_id_string = str(article['_id'])

    # article's html
    article_column_value = article[mongo_column]

    # index article's column in Elasticsearch
    res = es.index(
        index=elastic_index_name,
        doc_type='_doc',
        id=item_id_string, # document id in Elasticsearch == article id in articles collection
        document=json.dumps(
            {elastic_field: article_column_value}
        )
    )

    # insert into local MongoDB collection
    local_collection.insert_one({"_id": item_id_string, mongo_column: article_column_value})

# mongo cursor behaves like a file pointer - after read, rewind must be executed
cursor.rewind()
for article in cursor:
    links.append(article["link"])
local_collection = local_db[mongo_collection_crimemaps]
crime_maps_collection = db[mongo_collection_crimemaps]
cursor_crime_map = crime_maps_collection.find({"link": {"$in": links}}).limit(num_of_articles)
for article in cursor_crime_map:
    local_collection.insert_one(article)

print('Indexing finished.')

# ssh session has to be stopped in the end
session.stop()