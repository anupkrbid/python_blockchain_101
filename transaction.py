from collections import OrderedDict
from printable import Printable


class Transaction(Printable):
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_ordered_dict(self):
        return OrderedDict([("sender", self.sender), ("receiver", self.receiver), ("amount", self.amount)])
