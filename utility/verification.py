""" Provides verification helper methods. """
from utility.hash_util import get_hash_string_256
from wallet import Wallet


class Verification:
    """ A helper class which offers various static and clas-based verification """
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        open_tx = [transaction.to_ordered_dict()
                   for transaction in transactions]
        guess = f"{open_tx} {last_hash} {proof}".encode()
        guess_hash = get_hash_string_256(guess)
        return guess_hash[0:2] == "00"

    @classmethod
    def verify_chain(cls, blockchain, get_block_hash):
        """ Verify the current blockchain and return True if it's valid, False if not """
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
        sender_balance = get_balance()
        if check_funds:
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """ Verified all open transactions """
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])
