from flask import Flask, jsonify
from flipside import Flipside
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/data": {"origins": "http://localhost:3000"}})

flipside = Flipside("13ec68d6-a39d-4c4f-a2b9-fad92e6121a7", "https://api-v2.flipsidecrypto.xyz")

@app.route('/data', methods=['GET'])
def fetch_data():
    sql = """SELECT DATE(BLOCK_TIMESTAMP) as time, COUNT(TX_HASH) as value from optimism.core.fact_token_transfers group by DATE(BLOCK_TIMESTAMP) ORDER by DATE(BLOCK_TIMESTAMP)  limit 365;"""
    query_result_set = flipside.query(sql)

    # Extract only the necessary data for serialization
    data = []
    for row in query_result_set.rows:
        num_of_transactions = row[1]
        date = row[0]
        data.append({'value': num_of_transactions, 'time': date})

    return jsonify(data)

if __name__ == '__main__':
    app.run()
