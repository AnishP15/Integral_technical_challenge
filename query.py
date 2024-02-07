from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os 
import datetime
# My local endpoint: http://127.0.0.1:5000/api/accounts?account_id=0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97

app = Flask(__name__)

load_dotenv()

api_key = os.getenv("ETHERSCAN_API_KEY")

@app.route('/api/balance', methods=['GET'])
def get_token_balance():

    account_id = request.args.get('account_id')

    url = f"https://api.etherscan.io/api?module=account&action=balance&address={account_id}&tag=latest&apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return jsonify({"eth_balance":str(int(data["result"]) / (10 ** int(18)))})

    except requests.RequestException as e:
        return jsonify({"error": f"Error fetching data: {e}"}), 500


@app.route('/api/accounts', methods=['GET'])
def get_account_transactions():
    """
    Retrieve transactions associated with the account.

    Query Parameters:
        account_id(str): Ethereum account address.

    Returns:
        dict: A dictionary containing the transactions associated with the account.
    """
    account_id = request.args.get('account_id')

    if not account_id:
        return jsonify({"error": "Missing account_address parameter"}), 400

    try:

        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={account_id}&apikey={api_key}"
        
        response = requests.get(url)
        response.raise_for_status()   
        data = response.json()

        final_query = format_resp(data, account_id) 
        return final_query

    except requests.RequestException as e:
        return jsonify({"error": f"Error fetching data: {e}"}), 500


def format_resp(response: str, account_id: str):
    """
    Format data from etherscan into relevant fieldss

    Query Parameters:
        response: Raw response from Etherscan query of account_id
        account_id(str): Token contract address.

    Returns:
        dict: return formatted data dictionary.
    """
    
    formatted_data = []
    
    for transaction in response["result"]:
        timestamp_utc = datetime.datetime.utcfromtimestamp(int(transaction["timeStamp"]))

        formatted_transaction = {
            "transaction_idx": transaction["transactionIndex"],  
            "accountId": account_id,
            "toAddress": transaction["to"],
            "fromAddress": transaction["from"],
            "type": "deposit" if int(transaction["value"]) > 0 else "withdrawal",
            "amount": str(int(transaction["value"]) / (10 ** 18)),   
            "symbol": "ETH",   
            "decimal": 18,
            "timestamp": timestamp_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),   
            "txnHash": transaction["hash"]

        }
        
        formatted_data.append(formatted_transaction)
    
    formatted_response = {
        "data": formatted_data,
        "count": len(formatted_data)
    }

    return formatted_response

if __name__ == '__main__':
    app.run(debug=True)
