import functools
import json
import pickle

from block import Block
from transaction import Transaction
from utility.verification import Verification
from wallet import Wallet
from utility.hash_util import get_block_hash

# The reward given to miners (for creating a new block)
MINING_REWARD = 10


class Blockchain:
    """The Blockchain class manages the chain of blocks as well as open transactions and the node on which it's running.

    Attributes:
        :chain: The list of blocks
        :open_transactions (private): The list of open transactions
        :hosting_node: The connected node (which runs the blockchain).
    """

    def __init__(self, hosting_node_id) -> None:
        self.hosting_node_id = hosting_node_id
        # Our starting block for the blockchain
        genesis_block = Block(0, "", [], 100, 0)
        # Initializing our blockchain list
        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    # @chain.setter
    # def chain(self, value):
    #     self.__chain = value

    @property
    def open_transactions(self):
        return self.__open_transactions[:]

    # @open_transactions.setter
    # def open_transactions(self, value):
    #     pass

    def load_data(self):
        """ Initialize blockchain + open transaactions data """
        try:
            # with open("blockchain.txt", mode="rb") as f:
            #     file_content = f.read()
            #     blockchain, open_transactions = pickle.loads(
            #         file_content).values()
            #     self.__chain = blockchain
            #     self.__open_transactions = open_transactions
            with open("blockchain.txt", mode="r") as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                open_transactions = json.loads(file_content[1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx["sender"], tx["receiver"], tx["signature"], tx["amount"]) for tx in block["transactions"]]
                    updated_block = Block(
                        block["index"], block["previous_hash"], converted_tx, block["proof"], block['timestamp'])
                    updated_blockchain.append(updated_block)

                self.__chain = updated_blockchain

                self.__open_transactions = [Transaction(
                    tx["sender"], tx["receiver"], tx["signature"], tx["amount"]) for tx in open_transactions]
        except (IOError, IndexError, EOFError):
            print("IOError or IndexError Exception Handle")
        finally:
            print("Cleanup Code runs no matter what. Code succeeds or fails")

    def save_data(self):
        """ Save blockchain + open transactions snapshot to a file """
        try:
            # with open("blockchain.txt", mode="wb") as f:
            #     save_data = {
            #         "blockchain": self.__chain,
            #         "open_transactions": self.__open_transactions
            #     }
            #     f.write(pickle.dumps(save_data))
            with open("blockchain.txt", mode="w") as f:
                modified_blockchain = [
                    Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof,  block_el.timestamp) for block_el in self.chain]
                saveable_chain = [
                    block.__dict__ for block in modified_blockchain]
                # saveable_chain = [block.__dict__ for block in [
                #     Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof,  block_el.timestamp) for block_el in self.__chain]]
                savable_open_txs = [
                    tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_chain))
                f.write("\n")
                f.write(json.dumps(savable_open_txs))
        except IOError:
            print("Data Saving Failed")

    def proof_of_work(self):
        """ Generate a proof of work for the open transaction, last hash and proof """
        last_block = self.__chain[-1]
        last_hash = get_block_hash(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        recipient = self.hosting_node_id
        tx_debit_balances = [[tx.amount for tx in block.transactions if tx.sender == recipient]
                             for block in self.__chain]
        tx_debit_balance = functools.reduce(
            lambda acc, curr: acc + sum(curr), tx_debit_balances, 0)

        tx_credit_balances = [[tx.amount for tx in block.transactions if tx.receiver == recipient]
                              for block in self.__chain]
        tx_credit_balance = functools.reduce(
            lambda acc, curr: acc + sum(curr), tx_credit_balances, 0)

        tx_open_debit_balance = sum(
            [tx.amount for tx in self.__open_transactions if tx.sender == recipient])

        return tx_credit_balance - (tx_debit_balance + tx_open_debit_balance)

    def get_last_blockchain_value(self):
        """ Return the last value of the current blockchain """
        if len(self.chain) < 1:
            return None

        return self.chain[-1]

    def add_transaction(self, receiver, sender, signature, amount=1.0):
        """ Append a new value as well as the last blockchain value to the current blockchain

        Attribute:
            :sender: The sender of the coin
            :receiver: The receiver of the coin
            :signature: The signature of the transaction 
            :amount: The amount of coins sent
        """
        if self.hosting_node_id == None:
            return False

        transaction = Transaction(sender, receiver, signature, amount)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        global open_transactions

        if self.hosting_node_id == None:
            print("Mining Failed. Got no wallet?")
            pass

        last_block = self.__chain[-1]
        hashed_block = get_block_hash(last_block)
        proof = self.proof_of_work()
        tx_reward = Transaction(
            "MINING", self.hosting_node_id, "", MINING_REWARD)
        copied_transaction = self.__open_transactions[:]

        for tx in copied_transaction:
            if not Wallet.verify_transaction(tx):
                print("Transaction verification failed")
                return

        copied_transaction.append(tx_reward)
        rewared_block = Block(len(self.__chain), hashed_block,
                              copied_transaction, proof)

        self.__chain.append(rewared_block)
        open_transactions = []
        self.save_data()
