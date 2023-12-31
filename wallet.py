from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii


class Wallet:
    """Creates, loads and holds private and public keys. Manages transaction signing and verification."""

    def __init__(self, current_node_id):
        self.private_key = None
        self.public_key = None
        self.current_node_id = current_node_id

    def create_keys(self):
        """Create a new pair of private and public keys."""
        public_key, private_key = self.generate_keys()
        self.public_key = public_key
        self.private_key = private_key

    def save_keys(self):
        """Saves the keys to a file (wallet.txt)."""
        if self.public_key != None and self.private_key != None:
            try:
                with open("data/wallet-{}.txt".format(self.current_node_id), mode="w") as f:
                    f.write(self.public_key)
                    f.write("\n")
                    f.write(self.private_key)
                    return True
            except (IOError, IndexError):
                print("Saving wallet failed...")
                return False

    def load_keys(self):
        """Loads the keys from the wallet.txt file into memory."""
        try:
            with open("data/wallet-{}.txt".format(self.current_node_id), mode="r") as f:
                keys = f.readlines()
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
                return True
        except (IOError, IndexError):
            print("Loading wallet failed...")
            return False

    def generate_keys(self):
        """Generate a new pair of private and public key."""
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return ((binascii.hexlify(public_key.export_key(format="DER"))).decode("ascii"), (binascii.hexlify(private_key.export_key(format="DER"))).decode("ascii"))

    def sign_transaction(self, sender, receiver, amount):
        """Sign a transaction and return the signature.

        Arguments:
            :sender: The sender of the transaction.
            :receiver: The receiver of the transaction.
            :amount: The amount of the transaction.
        """
        signer = PKCS1_v1_5.new(RSA.import_key(
            binascii.unhexlify(self.private_key)))
        hashh = SHA256.new(f"{sender}{receiver}{amount}".encode("utf8"))
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
