from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)


@app.route("/", methods=["GET"])
def get_ui():
    return send_from_directory("ui", "node.html")


@app.route("/wallets/create/keys", methods=["POST"])
def create_wallet_keys():
    global blockchain
    wallet.create_keys()
    if wallet.save_keys():
        blockchain = Blockchain(wallet.public_key)
        success_res = {
            "message": "Wallet keys creation successful.",
            "funds": blockchain.get_balance(),
            "public_key": wallet.public_key,
            "private_key": wallet.private_key
        }
        return jsonify(success_res), 201
    else:
        error_res = {
            "message": "Wallet keys creation failed."
        }
        return jsonify(error_res), 400


@app.route("/wallets/load/keys", methods=["POST"])
def load_wallet_keys():
    global blockchain
    if wallet.load_keys() != None:
        blockchain = Blockchain(wallet.public_key)
        success_res = {
            "message": "Wallet keys loading successful",
            "funds": blockchain.get_balance(),
            "public_key": wallet.public_key,
            "private_key": wallet.private_key
        }
        return jsonify(success_res), 200
    else:
        error_res = {
            "message": "Wallet keys loading failed"
        }
        return jsonify(error_res), 400


@app.route("/wallets/balance", methods=["GET"])
def get_wallet_balance():
    balance = blockchain.get_balance()
    if balance != None:
        success_res = {
            "message": "Wallet balance fetching successful",
            "funds": balance
        }
        return jsonify(success_res), 200
    else:
        error_res = {
            "message": "Wallet balance fetching failed",
            "wallet_setup": wallet.public_key != None
        }
        return jsonify(error_res), 400


@app.route("/transactions", methods=["POST"])
def add_transaction():
    values = request.get_json()
    if not values:
        error_res = {
            "message": "No request data found"
        }
        return jsonify(error_res), 400

    required_fields = ["tx_receiver", "tx_amount"]
    if not all((field in values) for field in required_fields):
        error_res = {
            "message": "tx_receiver & tx_amount are requierd fields"
        }
        return jsonify(error_res), 400

    # Add the transaction amount to the blockchain
    tx_receiver = values["tx_receiver"]
    tx_amount = values["tx_amount"]
    signature = wallet.sign_transaction(wallet.public_key, tx_receiver,
                                        tx_amount)
    if blockchain.add_transaction(tx_receiver, wallet.public_key, signature,
                                  amount=tx_amount):
        success_res = {
            "message": "Transaction successful",
            "funds": blockchain.get_balance(),
            "transaction": {
                "sender": wallet.public_key,
                "receiver": tx_receiver,
                "amount": tx_amount
            }
        }
        return jsonify(success_res), 201
    else:
        error_res = {
            "message": "Transaction failed"
        }
        return jsonify(error_res), 400


@app.route("/transactions", methods=["GET"])
def get_open_transactions():
    dict_txs = [tx.__dict__ for tx in blockchain.open_transactions]
    success_res = {
        "message": "Open transactions fetch sucessful",
        "open_transaction": dict_txs
    }
    return jsonify(success_res), 200


@app.route("/blocks/mine", methods=["POST"])
def mine_block():
    mined_block = blockchain.mine_block()
    if mined_block != None:
        dict_block = mined_block.__dict__.copy()
        dict_block["transactions"] = [
            tx.__dict__ for tx in dict_block["transactions"]]
        success_res = {
            "message": "Block mining sucessful",
            "funds": blockchain.get_balance(),
            "block:": dict_block
        }
        return jsonify(success_res), 201
    else:
        error_res = {
            "message": "Block mining failed",
            "wallet_setup:": wallet.public_key != None
        }
        return jsonify(error_res), 400


@app.route("/blockchain", methods=["GET"])
def get_blockchain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block["transactions"] = [
            tx.__dict__ for tx in dict_block["transactions"]]

    success_res = {
        "message": "Blockchain fetch sucessful",
        "blockchain": dict_chain
    }
    return jsonify(success_res), 200


@app.route("/nodes", methods=["POST"])
def add_node():
    values = request.get_json()
    if not values:
        error_res = {
            "message": "No data found"
        }
        return jsonify(error_res), 400

    if "node" not in values:
        error_res = {
            "message": "No node data found"
        }
        return jsonify(error_res), 400

    blockchain.add_peer_node(values.get("node"))
    success_res = {
        "message": "Node addition sucessful",
        "nodes": list(blockchain.get_peer_nodes())
    }
    return jsonify(success_res), 200


@app.route("/nodes", methods=["GET"])
def get_nodes():
    blockchain.get_peer_nodes()
    success_res = {
        "message": "Nodes fetch sucessful",
        "nodes": list(blockchain.get_peer_nodes())
    }
    return jsonify(success_res), 200


@app.route("/nodes/<node_url>", methods=["DELETE"])
def remove_node(node_url):

    if node_url == "" or node_url == None:
        error_res = {
            "message": "No node data found"
        }
        return jsonify(error_res), 400

    blockchain.remove_peer_node(node_url)
    success_res = {
        "message": "Node removal sucessful",
        "nodes": list(blockchain.get_peer_nodes())
    }
    return jsonify(success_res), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
