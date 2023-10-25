""" This file contains the hash functions for the blockchain."""

import hashlib as hl
import json

def hash_string_256(string):
    """ Hashes a string using SHA256
    
    Arguments:
        :string: The string which should be hashed.
    """
    return hl.sha256(string).hexdigest()

# Hashes a block and returns a string representation of it
def hash_block(block):
    """ Hashes a block and returns a string representation of it 
    
    Arguments:
        :block: The block that should be hashed
    """
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
