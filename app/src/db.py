import os

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


class DatabaseEntities:
    mongodb_client: MongoClient
    main_database: Database
    papers_collection: Collection
    users_collection: Collection

    def define(self):
        self.mongodb_client = MongoClient(os.environ["MONGO_URI"])
        self.main_database = self.mongodb_client[os.environ["DB_NAME"]]
        self.papers_collection = self.main_database["dblpv13"]  # created from import
        self.users_collection = self.main_database[
            "users"
        ]  # create collection with users
        # create unique index for username
        self.users_collection.create_index("username", unique=True)

    def close(self):
        self.mongodb_client.close()


db = DatabaseEntities()
