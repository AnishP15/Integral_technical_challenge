import unittest
from db import TransactionStore
from pymongo import MongoClient

class TestTransactionStore(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['test_database']
        self.collection = self.db['test_accounts']

        self.ts = TransactionStore(db_name='test_database', collection_name='test_accounts')

    def test_insert_balance(self):

        account_id = '0x4AF6cB382DF144D989F984ad992109F936C20E4a'
        balance = 10

        self.ts.insert_balance(account_id, balance)

        account = self.collection.find_one({'account_id': account_id})

        self.assertIsNotNone(account)
        self.assertEqual(account['balance'], balance)

    def test_insert_transactions(self):
        
        account_id = '0x4AF6cB382DF144D989F984ad992109F936C20E4a'
        transactions = [
                {
                "accountId": "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97",
                "amount": "0.3",
                "decimal": 18,
                "fromAddress": "0x21a31ee1afc51d94c2efccaa2092ad1028285549",
                "symbol": "ETH",
                "timestamp": "2023-04-04T17:08:23.000000Z",
                "toAddress": "0x4838b106fce9647bdf1e7877bf73ce8b0bad5f97",
                "transaction_idx": "47",
                "txnHash": "0xb5b9e8281c99d88258931da08a67650a40684d9d81d3c01d759b1442a0734e85",
                "type": "deposit"
                },
                {
                "accountId": "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97",
                "amount": "0.0",
                "decimal": 18,
                "fromAddress": "0x4838b106fce9647bdf1e7877bf73ce8b0bad5f97",
                "symbol": "ETH",
                "timestamp": "2023-04-05T16:20:11.000000Z",
                "toAddress": "0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e",
                "transaction_idx": "213",
                "txnHash": "0x5b1718e8946bd55de3828e7828292a4aa17c38da8e7f836b9ea3d812a59c63d8",
                "type": "withdrawal"
                },
        ]

        self.ts.insert_transactions(account_id, transactions)

        account = self.collection.find_one({'account_id': account_id})

        self.assertIsNotNone(account)   
        self.assertEqual(account['transactions'], transactions)

    def tearDown(self):
        self.db.drop_collection('test_accounts')
        self.client.close()

if __name__ == '__main__':
    unittest.main()
