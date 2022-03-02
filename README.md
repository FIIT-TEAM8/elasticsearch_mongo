## How to run
  * git clone <url>
  * go to repository folder
  * python -m venv .\venv
  * .\venv\Scripts\activate
  * pip install -r requirements.txt
  * create your own mongo_db.env and es_indexer.env in configs folder based on their examples
  * docker-compose up -d
### Tests
  * cd ./test from working directory
  * python ./elastic_test.py # test Elasticsearch
  * python ./mongo_test.py # test MongoDB

## Elasticsearch configuration
  * Currently using one node with 1 shards and 1 replica
  * Standard analyzer with filtering english stop words and converting text to lowercase
  * This analyzer is used when indexing and querying data
  * Each document consists only from one field(text) and it's value isn't stored in elasticsearch
  * _source isn't stored too

## MongoDB configuration
  * MongoDB root user_name and password are defined in mongo_db.env file (only mongo_db.example.env is in repository)
 
## es_indexer configuration
  * SSH MongoDB tunneling, Local MongoDB connection, Elastisearch connection and other needed values are defined in es_indexer.env (only es_indexer.example.env is in repository)

