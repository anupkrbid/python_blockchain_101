from collections import OrderedDict
from utility.printable import Printable


class Transaction(Printable):
    """A trannsaction which can be added to a block in the blockchain.

    Attribute:
        :sender: The sender of the coin
        :receiver: The receiver of the coin
        :signature: The signature of the transaction 
        :amount: The amount of coins sent
    """

    def __init__(self, sender, receiver, signature, amount):
        self.sender = sender
        self.receiver = receiver
        self.signature = signature
        self.amount = amount

    def to_ordered_dict(self):
        """Converts this transaction into a (hashable) OrderedDict."""
        return OrderedDict([("sender", self.sender), ("receiver", self.receiver), ("amount", self.amount)])
