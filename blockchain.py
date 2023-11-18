import functools

# Initializing our blockchain list
MINING_REWARD = 10
GENESIS_BLOCK = {
    "previous_hash": "",
    "index": 0,
    "transactions": []
}
blockchain = [GENESIS_BLOCK]
open_transactions = []
recipients = {"Anup"}
owner = "Anup"


def get_balance(recipient):
    tx_debit_balances = [[tx["amount"] for tx in block['transactions'] if tx["sender"] == recipient]
                         for block in blockchain]
    # tx_debit_balance = sum([sum(bal) for bal in tx_debit_balances])
    tx_debit_balance = functools.reduce(
        lambda acc, curr: acc + sum(curr), tx_debit_balances, 0)

    tx_credit_balances = [[tx["amount"] for tx in block['transactions'] if tx["receiver"] == recipient]
                          for block in blockchain]
    # tx_credit_balance = sum([sum(bal) for bal in tx_credit_balances])
    tx_credit_balance = functools.reduce(
        lambda acc, curr: acc + sum(curr), tx_credit_balances, 0)

    tx_open_debit_balance = sum(
        [tx["amount"] for tx in open_transactions if tx["sender"] == recipient])

    return tx_credit_balance - (tx_debit_balance + tx_open_debit_balance)


def get_user_choice():
    return input("Your Choice: ")


def get_block_hash(block):
    return "-".join([str(block[key]) for key in block])


def get_last_blockchain_value():
    """ Return the last value of the current blockchain """
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])
    return sender_balance >= transaction["amount"]


def add_transaction(receiver, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the current blockchain

    Arguments:
        :sender: The sender of the coins.
        :receiver: The receiver of the coins.
        :amount: The amount of the coins.
    """
    transaction = {
        "sender": sender,
        "receiver": receiver,
        "amount": amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        recipients.add(sender)
        recipients.add(receiver)
        return True
    return False


def mine_block():
    global open_transactions
    last_block = blockchain[-1]
    hashed_block = get_block_hash(last_block)
    tx_reward = {
        "sender": "MINING",
        "receiver": owner,
        "amount": MINING_REWARD
    }
    copied_transaction = open_transactions[:]
    copied_transaction.append(tx_reward)
    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": copied_transaction
    }
    blockchain.append(block)
    open_transactions = []


def get_transaction_data():
    """ Return the input of the user (a new transaction amount) as a float """
    tx_receiver = input("Enter the receiver of the transaction: ")
    tx_return = float(input("Enter transaction amount please: "))
    return (tx_receiver, tx_return)


def print_blokchain():
    for block in blockchain:
        print("output block")
        print(block)
    else:
        print("-" * 20)


def verify_chain():
    # for (index, block) in enumerate(blockchain):
    for block_index in range(len(blockchain)):
        if block_index <= 0:
            continue

        current_block = blockchain[block_index]
        previous_block = blockchain[block_index - 1]
        previous_block_hash = get_block_hash(previous_block)
        if current_block["previous_hash"] != previous_block_hash:
            return False

    return True


waiting_for_input = True
while waiting_for_input:
    print("""Please Choose
        1: Add a new transaction value
        2: Mine a new block
        3: Output the blockchain blocks
        4: Output receivers
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
        print(recipients)
    elif choice == "h":
        if len(blockchain) > 0:
            blockchain[0] = {
                "previous_hash": "",
                "index": 0,
                "transactions": [{
                    "sender": "Max",
                    "receiver": "Manual",
                    "amount": 100
                }]
            }
    elif choice == "q":
        waiting_for_input = False
    else:
        print("Invalid choice, try again")

    if not verify_chain():
        print_blokchain()
        print("Blockchain coroupted!")
        break

    print("Balance of {}: {:6.2f}".format(owner, get_balance(owner)))
else:
    print("User Left Normally!")

print("Done!")
