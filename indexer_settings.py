import os
from dotenv import load_dotenv


if os.path.exists("./local.env") and os.path.exists("./remote.env"):
    env_file = open("remote.env").read() + open("local.env").read()
    open("./.env", "w").write(env_file)
    load_dotenv()

local_postgres_host = os.environ['POSTGRES_HOST'] or 22
local_postgres_port = os.environ['POSTGRES_PORT'] or 22
local_postgres_user = os.environ['POSTGRES_USER'] or 22
local_postgres_password = os.environ['POSTGRES_PASSWORD'] or 22
local_postgres_db = os.environ['REMOTE_POSTGRES_DATABASE'] or 22
remote_postgres_host = os.environ['REMOTE_POSTGRES_HOST'] or 22
remote_postgres_port = os.environ['REMOTE_POSTGRES_PORT'] or 22
remote_postgres_user = os.environ['REMOTE_POSTGRES_USER'] or 22
remote_postgres_password = os.environ['REMOTE_POSTGRES_PASSWORD'] or 22
remote_postgres_db = os.environ['REMOTE_POSTGRES_DATABASE'] or 22


local_mongo_host = os.environ['MONGO_HOST'] or 22
local_mongo_port = os.environ['MONGO_PORT'] or 22
local_mongo_user = os.environ['MONGO_INITDB_ROOT_USERNAME'] or 22
local_mongo_password = os.environ['MONGO_INITDB_ROOT_PASSWORD'] or 22
LOCAL_MONGO_CONN_STRING = "mongodb://{user}:{password}@{server_url}:{port}/".format(user=local_mongo_user, 
                                                                        password=local_mongo_password, 
                                                                        server_url=local_mongo_host, 
                                                                        port=local_mongo_port)
remote_mongo_host = os.environ['REMOTE_MONGO_HOST'] or 22
remote_mongo_port = os.environ['REMOTE_MONGO_PORT'] or 22
remote_mongo_user = os.environ['REMOTE_MONGO_USER'] or 22
remote_mongo_password = os.environ['REMOTE_MONGO_PASSWORD'] or 22
remote_mongo_database = os.environ['REMOTE_MONGO_DATABASE'] or 22
remote_mongo_collection = os.environ['REMOTE_MONGO_COLLECTION'] or 22
REMOTE_MONGO_CONN_STRING = "mongodb://{user}:{password}@{server_url}:{port}/".format(user=remote_mongo_user, 
                                                                        password=remote_mongo_password, 
                                                                        server_url=remote_mongo_host, 
                                                                        port=remote_mongo_port)

local_elastic_host = os.environ['ELASTIC_HOST'] or 22
local_elastic_port = os.environ['ELASTIC_PORT'] or 22
local_elastic_user = "elastic"
local_elastic_password = os.environ["ELASTIC_PASSWORD"] or "bruh"
elastic_collection = os.environ['ELASTIC_COLLECTION'] or 22
LOCAL_ELASTIC_CONNECTION_STRING = "{protocol}://{username}:{password}@{host}:{port}/".format(
    protocol="https",
    username=local_elastic_user,
    password=local_elastic_password,
    host=local_elastic_host,
    port=local_elastic_port
)

indexer_number_of_articles = int(os.environ['INDEXER_NUMBER_OF_ARTICLES']) or 22
indexer_wait_seconds = int(os.environ['INDEXER_WAIT_SECONDS']) or 22