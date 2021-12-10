import os
import unittest
import pymongo

class MongoTesting(unittest.TestCase):
    def test_insert_and_find(self):
        test_data = {
            "title": "Test",
            "published": "2021-12-10 14:51:21.362000",
            "link": "https://test.com/test",
            "html": "This is unit test insert one item into articles collection"
        }

        # mongo db configuration
        cluster = pymongo.MongoClient(
            host='localhost:27017',
            serverSelectionTimeoutMS = 3000,
            username=os.environ['MONGO_INITDB_ROOT_USERNAME'] or 'root',
            password=os.environ['MONGO_INITDB_ROOT_PASSWORD'] or 'password'
        )

        # connect to admin DB in Mongo
        db = cluster['admin']

        # connect to 'articles' collection, MongoDB will create one if it doesn't exists
        articles_collection = db['articles']

        # store test document
        return_value = articles_collection.insert_one(test_data)

        # test if document was successfully stored
        self.assertEqual(True, return_value.acknowledged)

        # retrieve lastly added document
        item = articles_collection.find_one(
            sort=[( '_id', pymongo.DESCENDING )]
        )

        # test if document has right data
        for key, value in item.items():
            if key != '_id':
                self.assertEqual(value, test_data[key])


if __name__ == '__main__':
    working_directory = os.getcwd()
    parent_directory = os.path.abspath(os.path.join(working_directory, os.pardir))

    # load mogno_db.env file
    with open(parent_directory + '/mongo_db.env', 'r') as env_file:
        lines = env_file.readlines()

        for line in lines:
            line = line.strip('\n')
            split = line.split('=')

            # set enviroment variables from mongo_db.env file
            os.environ[split[0]] = split[1]

    # start unit tests
    unittest.main()