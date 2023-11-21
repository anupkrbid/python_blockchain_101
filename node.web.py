from flask import Flask, jsonify
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)


@app.route("/", methods=["GET"])
def get_ui():
    return "This works"


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

    return "This works"


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

    return jsonify(dict_chain), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
