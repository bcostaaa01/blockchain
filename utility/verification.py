""" Provides verification helper methods. """

from utility.hash_util import hash_string_256, hash_block


class Verification:
    # Validate proof of work
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        """
        Validate a proof of work number and see if it solves the puzzle algorithm (two leading 0s)
        """
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        return guess_hash[0:2] == '00'
    
    @classmethod
    def verify_chain(self, blockchain):
        """
        Verify the current blockchain and return True if it's valid, False otherwise
        """
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of work is invalid")
                return False
        return True
    
    @staticmethod
    # Verify the transaction
    def verify_transaction(transaction, get_balance):
        """
        Verify a transaction by checking whether the sender has sufficient coins.
        """
        sender_balance = get_balance(transaction.sender)
        return sender_balance >= transaction.amount
    
    @classmethod
    # Verify all open transactions
    def verify_transactions(cls, open_transactions, get_balance):
        """
        Verify all open transactions and return True if they're all valid, False otherwise
        """
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])