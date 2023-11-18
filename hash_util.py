import hashlib
import json


def get_hash_string_256(json_string):
    return hashlib.sha256(json_string).hexdigest()


def get_block_hash(block):
    """ Hashes a block and returns a string representation  of it.

    Arguments:
        :block: The block that should be hashed.
    """
    json_string_block = json.dumps(block, sort_keys=True).encode()
    return get_hash_string_256(json_string_block)
