# Initializing our blockchain list
blockchain = []


def get_last_blockchain_value():
    """ Return the last value of the current blockchain """
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction=[1]):
    """ Append a new value as well as the last blockchain value to the current blockchain

    Arguments:
        :transaction_amount: The amount the should be added.
        :last_transaction: The last blockchain transaction (default [1])
    """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    """ Return the input of the user (a new transaction amount) as a float """
    return float(input("Enter transaction amount: "))


def get_user_choice():
    return input("Your Choice: ")


def print_blokchain():
    for block in blockchain:
        print("output block")
        print(block)
    else:
        print("-" * 20)


def verify_chain():
    for block_index in range(len(blockchain)):
        current_block = blockchain[block_index]
        previous_block = blockchain[block_index - 1]
        if block_index > 0 and current_block[0] != previous_block:
            return False

    # block_index = 0
    # for block in blockchain:
    #     if block_index > 0 and block[0] != blockchain[block_index-1]:
    #         return False
    #     block_index += 1

    return True

# tx_amount = get_transaction_value()
# add_transaction(tx_amount)


waiting_for_input = True
while waiting_for_input:
    print("""Please Choose
        1: Add a new transaction value
        2: Output the blockchain blocks
        h: Manipulate the chain
        q: Quit""")
    choice = get_user_choice()
    if choice == "1":
        tx_amount = get_transaction_value()
        add_transaction(last_transaction=get_last_blockchain_value(),
                        transaction_amount=tx_amount)
        # add_value(tx_amount, get_last_blockchain_value())
    elif choice == "2":
        print_blokchain()
    elif choice == "h":
        if len(blockchain) > 0:
            blockchain[0] = [2]
    elif choice == "q":
        waiting_for_input = False
    else:
        print("Invalid choice, try again")

    if not verify_chain():
        print_blokchain()
        print("Blockchain coroupted!")
        break
else:
    print("User Left Normally!")

print("Done!")
