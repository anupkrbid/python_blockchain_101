from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii


class Wallet:
    """Creates, loads and holds private and public keys. Manages transaction signing and verification."""

    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        """Create a new pair of private and public keys."""
        public_key, private_key = self.generate_keys()
        self.public_key = public_key
        self.private_key = private_key
        self.save_keys()

    def save_keys(self):
        """Saves the keys to a file (wallet.txt)."""
        if self.public_key != None and self.private_key != None:
            try:
                with open("wallet.txt", mode="w") as f:
                    f.write(self.public_key)
                    f.write("\n")
                    f.write(self.private_key)
            except (IOError, IndexError):
                print("Saving wallet failed...")

    def load_keys(self):
        """Loads the keys from the wallet.txt file into memory."""
        try:
            with open("wallet.txt", mode="r") as f:
                keys = f.readlines()
                self.public_key = keys[0][:-1]
                self.privat_key = keys[1]
        except (IOError, IndexError):
            print("Loading wallet failed...")

    def generate_keys(self):
        """Generate a new pair of private and public key."""
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return ((binascii.hexlify(public_key.export_key(format="DER"))).decode("ascii"), (binascii.hexlify(private_key.export_key(format="DER"))).decode("ascii"))

    def sign_transaction(self, sender, recipient, amount):
        """Sign a transaction and return the signature.

        Arguments:
            :sender: The sender of the transaction.
            :recipient: The recipient of the transaction.
            :amount: The amount of the transaction.
        """
        signer = PKCS1_v1_5.new(RSA.import_key(
            binascii.unhexlify(self.private_key)))
        hashh = SHA256.new(f"{sender}{recipient}{amount}".encode("utf8"))
        signature = signer.sign(hashh)
        return binascii.hexlify(signature).decode("ascii")

    @staticmethod
    def verify_transaction(transaction):
        """Verify the signature of a transaction.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        if transaction.sender == "MINING":
            return True

        public_key = RSA.import_key(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        hashh = SHA256.new(
            (str(transaction.sender) + str(transaction.receiver) + str(transaction.amount)).encode("utf8"))
        return verifier.verify(hashh, binascii.unhexlify(transaction.signature))
