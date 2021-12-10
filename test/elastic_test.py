import os
import time
import json
import unittest
from elasticsearch import Elasticsearch

class ElasticsearchTesting(unittest.TestCase):
    def test_index(self):
        # elasticsearch configuration
        es = Elasticsearch(HOST="http://localhost", PORT=9200)

        # create index if not exists
        if not es.indices.exists(index='articles_index'):
            working_directory = os.getcwd()
            parent_directory = os.path.abspath(os.path.join(working_directory, os.pardir))
            # firstly load index configuration
            with open(parent_directory + '/articles_index_config.json') as articles_config_file:
                # load index configuration as json
                configuration = json.load(articles_config_file)

                # create index
                res = es.indices.create(index="articles_index", settings=configuration["settings"])
                
                # test if index was successfully created
                self.assertEqual(res['acknowledged'], True)

        test_data = "Test sentence name Elasticsearch"
        test_id = '1'

        # index test_data in elasticsearch
        res = es.index(
            index='articles_index',
            doc_type='_doc',
            id=test_id,
            document=json.dumps(
                {"text": test_data}
            )
        )

        # test if sentence was successfully indexed
        self.assertEqual(res['result'], 'created')

        time.sleep(2)

        search_query = {
            "multi_match": {
                "query": "",
                "fields": ["text"]
            }
        }

        for word in test_data.split(' '):
            # change searching word in search query
            search_query['multi_match']['query'] = word

            # search in index based on query
            res = es.search(index="articles_index", query=search_query)

            # test if document was find in index and has proper id
            id = res['hits']['hits'][0]['_id']

            self.assertEqual(id, test_id)


if __name__ == '__main__':
    # start unit tests
    unittest.main()