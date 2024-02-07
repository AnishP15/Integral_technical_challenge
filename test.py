import unittest
from query import app
from flask import json


class TestQueries(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_account_transactions(self):
        account_id = "0x4AF6cB382DF144D989F984ad992109F936C20E4a"  # Example account id
        response = self.app.get(f'/api/accounts?account_id={account_id}')
        data = json.loads(response.data.decode('utf-8'))


       # Each element of data should have the 10 fields we query for
        for tx in data['data']:
            self.assertEqual(len(tx), 10)
        
        self.assertIn('count', data)

    def test_get_account_balance(self):
        account_id = "0x4AF6cB382DF144D989F984ad992109F936C20E4a" 
        response = self.app.get(f'/api/balance?account_id={account_id}')
        data = json.loads(response.data.decode('utf-8'))
        
        # Each account_id should have associate balance
        self.assertIn('eth_balance', data)

if __name__ == '__main__':
    unittest.main()
