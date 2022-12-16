import os

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


class DatabaseEntities:
    mongodb_client: MongoClient
    main_database: Database
    papers_collection: Collection
    users_collection: Collection
    authors_collection: Collection
    tags_collection: Collection
    author2author: Collection

    def define(self):
        self.mongodb_client = MongoClient(os.environ["MONGO_URI"])
        self.main_database = self.mongodb_client[os.environ["DB_NAME"]]
        self.papers_collection = self.main_database["dblpv13"]  # created from import
        self.users_collection = self.main_database[
            "users"
        ]  # create collection with users
        if "authors" not in self.main_database.list_collection_names():
            self.main_database.command(
                "create",
                "authors",
                viewOn="dblpv13",
                pipeline=[
                    {"$unwind": "$authors"},
                    {
                        "$group": {
                            "_id": "$authors._id",
                            "name": {"$first": "$authors.name"},
                            # "org": "$authors.org",
                        }
                    },
                ],
            )
        self.authors_collection = self.main_database["authors"]
        self.tags_collection = self.main_database["tags"]
        self.author2author = self.main_database["author2author"]

        self.users_collection.create_index("username", unique=True)
        self.users_collection.create_index("dblpv13.title")
        self.users_collection.create_index("dblpv13.abstract")
        self.users_collection.create_index("dblpv13.keywords")
        self.users_collection.create_index("dblpv13.authors.name")
        self.users_collection.create_index("dblpv13.venue.raw")

    def close(self):
        self.mongodb_client.close()


db = DatabaseEntities()
