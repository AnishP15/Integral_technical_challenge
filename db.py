from pymongo import MongoClient
from flask import json
from bson import json_util

class TransactionStore:
    def __init__(self, db_name='account_database', collection_name='accounts', connection_string='mongodb://localhost:27017/'):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_balance(self, account_id, balance):
        self.collection.update_one({'account_id': account_id}, {'$set': {'balance': balance}}, upsert=True)

    def insert_transactions(self, account_id, transactions):
        self.collection.update_one({'account_id': account_id}, {'$set': {'transactions': transactions}}, upsert=True)

    def get_account(self, account_id):
        return self.collection.find_one({'account_id': account_id})

    def get_all_data(self):
        cursor = self.collection.find()
        data = [json.loads(json_util.dumps(document)) for document in cursor]
        return json.dumps(data)