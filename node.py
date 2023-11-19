from uuid import uuid4
from verification import Verification
from blockchain import Blockchain
from block import Block
from hash_util import get_block_hash


class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.id = "Anup"
        self.blockchain = Blockchain(self.id)

    def get_user_choice(self):
        return input("Your Choice: ")

    def get_transaction_data(self):
        """ Return the input of the user (a new transaction amount) as a float """
        tx_receiver = input("Enter the receiver of the transaction: ")
        tx_return = float(input("Enter transaction amount please: "))
        return (tx_receiver, tx_return)

    def print_blokchain(self):
        print("-" * 100)
        for block in self.blockchain.chain:
            print(block)
        else:
            print("-" * 100)

    def listen_for_input(self):
        verification = Verification()
        waiting_for_input = True
        while waiting_for_input:
            print("""Please Choose
                1: Add a new transaction value
                2: Mine a new block
                3: Output the blockchain blocks
                4: Verify all transactions
                h: Manipulate the chain
                q: Quit""")
            choice = self.get_user_choice()
            if choice == "1":
                tx_data = self.get_transaction_data()
                tx_receiver, tx_amount = tx_data
                if self.blockchain.add_transaction(tx_receiver, self.id,
                                                   amount=tx_amount):
                    print("Transaction Successful")
                else:
                    print("Transacion Failed")
            elif choice == "2":
                self.blockchain.mine_block()
            elif choice == "3":
                self.print_blokchain()
            elif choice == "4":
                if verification.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
                    print("All transactions verification successful")
                else:
                    print("All transactions verification failed")
            elif choice == "h":
                if len(self.blockchain) > 0:
                    tampered_block = Block(0, "tampered", [], 100, 1)
                    self.blockchain[0] = tampered_block
            elif choice == "q":
                waiting_for_input = False
            else:
                print("Invalid choice, try again")

            if not verification.verify_chain(self.blockchain.chain, get_block_hash):
                self.print_blokchain()
                print("Blockchain coroupted!")
                break

            print("Balance of {}: {:6.2f}".format(
                self.id, self.blockchain.get_balance(self.id)))
        else:
            print("User Left Normally!")

        print("Done!")


node = Node()
node.listen_for_input()