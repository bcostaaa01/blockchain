# Imports
from functools import reduce
import hashlib as hl
import json

# File imports
from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet


# Initialize the reward for mining a new block
MINING_REWARD = 10

print(__name__)

class Blockchain:
    def __init__(self, hosting_node_id):
        # Our starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing our (empty) blockchain list
        self.__chain = [genesis_block]
        # Initialize the open transactions list
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id
        
        
    # Get the blockchain list
    @property
    def chain(self):
        return self.__chain[:]
        
        
    # Set the blockchain list
    @chain.setter
    def chain(self, val):
        self.__chain = val
    
    
    # Get the open transactions list
    def get_open_transactions(self):
        return self.__open_transactions[:]
        

    # Save the last transaction in a variable
    def load_data(self):
        """ 
        Initialize blockchain + open transactions data from a file 
        """
        try:
            with open('blockchain.txt', mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        except (IOError, IndexError):
            pass
        finally:
            print("Cleanup!")
            # f.close()


    # Save the last transaction in a variable
    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
        except IOError:
            print("Saving failed!")


    # Proof of work
    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof


    # Get the balance of a participant
    def get_balance(self):
        """
        Function to get the balance of a participant.
        """
        if self.hosting_node == None:
            return None
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        return amount_received - amount_sent


    # Return the last value of the current blockchain
    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]
    

    # Add a new value as well as the last blockchain value to the blockchain
    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """ Append a new value as well as the last blockchain value to the blockchain
        
        Arguments
            :recipient: The recipient of the coins
            :sender: The sender of the coins
            :signature: The signature of the transaction
            :transaction_amount: The amount that should be added
        """
        if self.hosting_node == None:
            return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):   
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        else:
            return False
    

    # Mine a new block
    def mine_block(self):
        """ Mine a new block """
        if self.hosting_node == None:
            return None
        last_block = self.__chain[-1]
        # Fetch the currently last block of the blockchain
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.hosting_node, '', MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):  # Assuming you have a 'wallet' instance
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block
