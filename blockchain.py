import functools
import json
import pickle

from block import Block
from transaction import Transaction
from verification import Verification
from hash_util import get_block_hash

# Initializing our blockchain list
MINING_REWARD = 10
blockchain = []
open_transactions = []
owner = "Anup"
verification = Verification()

# [{"previous_hash": "", "index": 0, "transactions": [], "proof": 100}]
# []


def load_data():
    global blockchain
    global open_transactions
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

            blockchain = updated_blockchain

            open_transactions = [Transaction(
                tx["sender"], tx["receiver"], tx["amount"]) for tx in open_transactions]
    except (IOError, IndexError):
        genesis_block = Block(0, "", [], 100, 0)
        blockchain = [genesis_block]
    finally:
        print("Code runds no matter what. Code succeeds or fails")


load_data()


def save_data():
    try:
        # with open("blockchain.txt", mode="wb") as f:
        #     save_data = {
        #         "blockchain": blockchain,
        #         "open_transactions": open_transactions
        #     }
        #     f.write(pickle.dumps(save_data))
        with open("blockchain.txt", mode="w") as f:
            modified_blockchain = [
                Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof) for block_el in blockchain]
            saveable_chain = [block.__dict__ for block in modified_blockchain]
            savable_open_txs = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_chain))
            f.write("\n")
            f.write(json.dumps(savable_open_txs))
    except IOError:
        print("Data Saving Failed")


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = get_block_hash(last_block)
    proof = 0
    while not verification.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(recipient):
    tx_debit_balances = [[tx.amount for tx in block.transactions if tx.sender == recipient]
                         for block in blockchain]
    tx_debit_balance = functools.reduce(
        lambda acc, curr: acc + sum(curr), tx_debit_balances, 0)

    tx_credit_balances = [[tx.amount for tx in block.transactions if tx.receiver == recipient]
                          for block in blockchain]
    tx_credit_balance = functools.reduce(
        lambda acc, curr: acc + sum(curr), tx_credit_balances, 0)

    tx_open_debit_balance = sum(
        [tx.amount for tx in open_transactions if tx.sender == recipient])

    return tx_credit_balance - (tx_debit_balance + tx_open_debit_balance)


def get_user_choice():
    return input("Your Choice: ")


def get_last_blockchain_value():
    """ Return the last value of the current blockchain """
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def add_transaction(receiver, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the current blockchain

    Arguments:
        :sender: The sender of the coins.
        :receiver: The receiver of the coins.
        :amount: The amount of the coins.
    """
    transaction = Transaction(sender, receiver, amount)
    if verification.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def mine_block():
    global open_transactions
    last_block = blockchain[-1]
    hashed_block = get_block_hash(last_block)
    proof = proof_of_work()
    tx_reward = Transaction("MINING", owner, MINING_REWARD)
    copied_transaction = open_transactions[:]
    copied_transaction.append(tx_reward)
    rewared_block = Block(len(blockchain), hashed_block,
                          copied_transaction, proof)
    blockchain.append(rewared_block)
    open_transactions = []
    save_data()


def get_transaction_data():
    """ Return the input of the user (a new transaction amount) as a float """
    tx_receiver = input("Enter the receiver of the transaction: ")
    tx_return = float(input("Enter transaction amount please: "))
    return (tx_receiver, tx_return)


def print_blokchain():
    print("-" * 100)
    for block in blockchain:
        print(block)
    else:
        print("-" * 100)


waiting_for_input = True
while waiting_for_input:
    print("""Please Choose
        1: Add a new transaction value
        2: Mine a new block
        3: Output the blockchain blocks
        4: Verify all transactions
        h: Manipulate the chain
        q: Quit""")
    choice = get_user_choice()
    if choice == "1":
        tx_data = get_transaction_data()
        tx_receiver, tx_amount = tx_data
        if add_transaction(tx_receiver,
                           amount=tx_amount):
            print("Transaction Successful")
        else:
            print("Transacion Failed")
    elif choice == "2":
        mine_block()
    elif choice == "3":
        print_blokchain()
    elif choice == "4":
        if verification.verify_transactions(open_transactions, get_balance):
            print("All transactions verification successful")
        else:
            print("All transactions verification failed")
    elif choice == "h":
        if len(blockchain) > 0:
            tampered_block = Block(0, "tampered", [], 100, 1)
            blockchain[0] = tampered_block
    elif choice == "q":
        waiting_for_input = False
    else:
        print("Invalid choice, try again")

    if not verification.verify_chain(blockchain, get_block_hash):
        print_blokchain()
        print("Blockchain coroupted!")
        break

    print("Balance of {}: {:6.2f}".format(owner, get_balance(owner)))
else:
    print("User Left Normally!")

print("Done!")
