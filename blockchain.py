import functools
import json
import pickle

from block import Block
from transaction import Transaction
from verification import Verification
from hash_util import get_block_hash

# The reward given to miners (for creating a new block)
MINING_REWARD = 10


class Blockchain:
    def __init__(self, hosting_node_id) -> None:
        self.hosting_node_id = hosting_node_id
        # Our starting block for the blockchain
        genesis_block = Block(0, "", [], 100, 0)
        # Initializing our blockchain list
        self.chain = [genesis_block]
        self.open_transactions = []
        self.load_data()

    def load_data(self):
        """ Initialize blockchain + open transaactions data """
        try:
            # with open("blockchain.txt", mode="rb") as f:
            #     global blockchain
            #     global open_transactions

            #     file_content = f.read()
            #     blockchain, open_transactions = pickle.loads(file_content).values()
            with open("blockchain.txt", mode="r") as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                open_transactions = json.loads(file_content[1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx["sender"], tx["receiver"], tx["amount"]) for tx in block["transactions"]]
                    updated_block = Block(
                        block["index"], block["previous_hash"], converted_tx, block["proof"])
                    updated_blockchain.append(updated_block)

                self.chain = updated_blockchain

                self.open_transactions = [Transaction(
                    tx["sender"], tx["receiver"], tx["amount"]) for tx in open_transactions]
        except (IOError, IndexError):
            print("IOError or IndexError Exception Handle")
        finally:
            print("Cleanup Code runs no matter what. Code succeeds or fails")

    def save_data(self):
        """ Save blockchain + open transactions snapshot to a file """
        try:
            # with open("blockchain.txt", mode="wb") as f:
            #     save_data = {
            #         "blockchain": blockchain,
            #         "open_transactions": open_transactions
            #     }
            #     f.write(pickle.dumps(save_data))
            with open("blockchain.txt", mode="w") as f:
                # modified_blockchain = [
                #     Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof) for block_el in self.chain]
                # saveable_chain = [
                #     block.__dict__ for block in modified_blockchain]
                saveable_chain = [block.__dict__ for block in [
                    Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof) for block_el in self.chain]]
                savable_open_txs = [
                    tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(saveable_chain))
                f.write("\n")
                f.write(json.dumps(savable_open_txs))
        except IOError:
            print("Data Saving Failed")

    def proof_of_work(self):
        """ Generate a proof of work for the open transaction, last hash and proof """
        last_block = self.chain[-1]
        last_hash = get_block_hash(last_block)
        proof = 0
        while not Verification.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        recipient = self.hosting_node_id
        tx_debit_balances = [[tx.amount for tx in block.transactions if tx.sender == recipient]
                             for block in self.chain]
        tx_debit_balance = functools.reduce(
            lambda acc, curr: acc + sum(curr), tx_debit_balances, 0)

        tx_credit_balances = [[tx.amount for tx in block.transactions if tx.receiver == recipient]
                              for block in self.chain]
        tx_credit_balance = functools.reduce(
            lambda acc, curr: acc + sum(curr), tx_credit_balances, 0)

        tx_open_debit_balance = sum(
            [tx.amount for tx in self.open_transactions if tx.sender == recipient])

        return tx_credit_balance - (tx_debit_balance + tx_open_debit_balance)

    def get_last_blockchain_value(self):
        """ Return the last value of the current blockchain """
        if len(self.chain) < 1:
            return None

        return self.chain[-1]

    def add_transaction(self, receiver, sender, amount=1.0):
        """ Append a new value as well as the last blockchain value to the current blockchain

        Arguments:
            :sender: The sender of the coins.
            :receiver: The receiver of the coins.
            :amount: The amount of the coins.
        """
        transaction = Transaction(sender, receiver, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        global open_transactions
        last_block = self.chain[-1]
        hashed_block = get_block_hash(last_block)
        proof = self.proof_of_work()
        tx_reward = Transaction("MINING", self.hosting_node_id, MINING_REWARD)
        copied_transaction = self.open_transactions[:]
        copied_transaction.append(tx_reward)
        rewared_block = Block(len(self.chain), hashed_block,
                              copied_transaction, proof)
        self.chain.append(rewared_block)
        open_transactions = []
        self.save_data()
