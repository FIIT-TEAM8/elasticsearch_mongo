## How to run
  * git clone <url>
  * go to repository folder
  * docker-compose up -d

## Elasticsearch configuration
  * Currently using one node with 1 shards and 1 replica
  * Standard analyzer with filtering english stop words and converting text to lowercase
  * This analyzer is used when indexing and querying data
  * Each document consists only from one field(text) and it's value isn't stored in elasticsearch
  * _source isn't stored too

## MongoDB configuration
  * MongoDB root user_name and password are defined in mongo_db.env file (only mongo_db.example.env is in repository)
  * Scripts connects to 'articles' collection or creates a new one in 'admin' db.

