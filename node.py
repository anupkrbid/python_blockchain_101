from uuid import uuid4
from blockchain import Blockchain
from block import Block
from utility.hash_util import get_block_hash
from utility.verification import Verification
from wallet import Wallet


class Node:
    """The node which runs the local blockchain instance.

    Attributes:
        :id: The id of the node.
        :blockchain: The blockchain which is run by this node.
    """

    def __init__(self):
        # self.id = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_user_choice(self):
        """Prompts the user for its choice and return it."""
        return input("Your Choice: ")

    def get_transaction_data(self):
        """Return the input of the user (a new transaction amount) as a float."""
        # Get the user input, transform it from a string to a float and store it in user_input
        tx_receiver = input("Enter the receiver of the transaction: ")
        tx_return = float(input("Enter transaction amount please: "))
        return (tx_receiver, tx_return)

    def print_blokchain(self):
        """Output all blocks of the blockchain."""
        # Output the blockchain list to the console
        print("-" * 100)
        for block in self.blockchain.chain:
            print(block)
        else:
            print("-" * 100)

    def listen_for_input(self):
        """Starts the node and waits for user input."""
        waiting_for_input = True
        # A while loop for the user input interface
        # It's a loop that exits once waiting_for_input becomes False or when break is called
        while waiting_for_input:
            print("""Please Choose
                1: Add a new transaction value
                2: Mine a new block
                3: Output the blockchain blocks
                4: Verify all transactions
                5: Create wallet
                6: Load wallet 
                7: Save wallet keys
                h: Manipulate the chain
                q: Quit""")
            choice = self.get_user_choice()
            if choice == "1":
                tx_data = self.get_transaction_data()
                tx_receiver, tx_amount = tx_data
                # Add the transaction amount to the blockchain
                signature = self.wallet.sign_transaction(self.wallet.public_key, tx_receiver,
                                                         tx_amount)
                if self.blockchain.add_transaction(tx_receiver, self.wallet.public_key, signature,
                                                   amount=tx_amount):
                    print("Transaction Successful")
                else:
                    print("Transacion Failed")
            elif choice == "2":
                self.blockchain.mine_block()
            elif choice == "3":
                self.print_blokchain()
            elif choice == "4":
                if Verification.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
                    print("All transactions verification successful")
                else:
                    print("All transactions verification failed")
            elif choice == "5":
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif choice == "6":
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif choice == "7":
                self.wallet.save_keys()
            elif choice == "h":
                if len(self.blockchain) > 0:
                    tampered_block = Block(0, "tampered", [], 100, 1)
                    self.blockchain[0] = tampered_block
            elif choice == "q":
                # This will lead to the loop to exist because it's running condition becomes False
                waiting_for_input = False
            else:
                print("Invalid choice, try again")

            if not Verification.verify_chain(self.blockchain.chain, get_block_hash):
                self.print_blokchain()
                print("Blockchain coroupted!")
                # Break out of the loop
                break

            print("Balance of {}: {:6.2f}".format(
                self.wallet.public_key, self.blockchain.get_balance()))
        else:
            print("User Left Normally!")

        print("Done!")


if __name__ == "__main__":
    node = Node()
    node.listen_for_input()
