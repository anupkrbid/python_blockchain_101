import hashlib
import json

__all__ = ["get_hash_string_256", "get_block_hash"]  # allowed exports


def get_hash_string_256(json_string):
    """ Create a SHA256 hash for a given input string.

    Arguments:
        :string: The string which should be hashed.
    """
    return hashlib.sha256(json_string).hexdigest()


def get_block_hash(block):
    """ Hashes a block and returns a string representation  of it.

    Arguments:
        :block: The block that should be hashed.
    """
    hashable_block = block.__dict__.copy()
    hashable_block["transactions"] = [tx.to_ordered_dict()
                                      for tx in block.transactions]
    json_string_block = json.dumps(hashable_block, sort_keys=True).encode()
    return get_hash_string_256(json_string_block)
