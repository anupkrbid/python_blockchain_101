""" Provides verification helper methods. """
from utility.hash_util import get_hash_string_256
from wallet import Wallet


class Verification:
    """A helper class which offers various static and clas-based verification."""
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        """Validate a proof of work number and see if it solves the puzzle algorithm (two leading 0s)

        Arguments:
            :transactions: The transactions of the block for which the proof is created.
            :last_hash: The previous block's hash which will be stored in the current block.
            :proof: The proof number we're testing.
        """
        open_tx = [transaction.to_ordered_dict()
                   for transaction in transactions]
        # Create a string with all the hash inputs
        guess = f"{open_tx} {last_hash} {proof}".encode()
        # Hash the string
        # IMPORTANT: This is NOT the same hash as will be stored in the previous_hash. It's a not a block's hash. It's only used for the proof-of-work algorithm.
        guess_hash = get_hash_string_256(guess)
        # Only a hash (which is based on the above inputs) which starts with two 0s is treated as valid
        # This condition is of course defined by you. You could also require 10 leading 0s - this would take significantly longer (and this allows you to control the speed at which new blocks can be added)
        return guess_hash[0:2] == "00"

    @classmethod
    def verify_chain(cls, blockchain, get_block_hash):
        """Verify the current blockchain and return True if it's valid, False otherwise."""
        # for (index, block) in enumerate(blockchain):
        for block_index in range(len(blockchain)):
            if block_index <= 0:
                continue

            current_block = blockchain[block_index]
            previous_block = blockchain[block_index - 1]
            previous_block_hash = get_block_hash(previous_block)
            if current_block.previous_hash != previous_block_hash:
                return False
            if not cls.valid_proof(current_block.transactions[:-1], current_block.previous_hash, current_block.proof):
                print('Proof of work in invalid')
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        """Verify a transaction by checking whether the sender has sufficient coins.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        sender_balance = get_balance(transaction.sender)
        if check_funds:
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """Verified all open transactions."""
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])
