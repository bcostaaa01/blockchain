from utility.verification import Verification
from blockchain import Blockchain
from uuid import uuid4
from wallet import Wallet


class Node:
    def __init__(self):
        # self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.blockchain = None
        
        
    # Get the transaction amount from the user and add it to the blockchain
    def get_transaction_value(self):
        """ 
        Returns the input of the user (a new transaction amount) as a float 
        """
        tx_recipient = input("Enter the recipient of the transaction: ")
        tx_amount = float(input("Your transaction amount please: "))
        return tx_recipient, tx_amount


    # Get the user input, transform it from a string to a float and add it to the blockchain
    def get_user_choice(self):
        """
        Get the user choice and transform it from a string to a float
        """
        user_input = input("Your choice: ")
        return user_input
    

    # Output the blockchain list to the console
    def print_blockchain_elements(self):
        """
        Output all blocks of the blockchain
        """
        for block in self.blockchain.chain:
            print("Outputting Block")
            print(block)
        else:
            print("-" * 20)   
             
    
    # Listen for user input
    def listen_for_input(self):
        """
        Wait for and handle user input
        """
        waiting_for_input = True
        
        while waiting_for_input:
            print("Please choose")
            print("1: Add a new transaction value")
            print("2: Mine a new block")
            print("3: Output the blockchain blocks")
            print("4: Check transaction validity")
            print("5: Create wallet")
            print("6: Load wallet")
            print("q: Quit")
            user_choice = self.get_user_choice()
            
            if user_choice == "1":
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                # Add transaction amount to the blockchain
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, amount=amount):
                    print("Added transaction!")
                else:
                    print("Transaction failed!")
                print(self.blockchain.get_open_transactions())
            elif user_choice == "2":
                if not self.blockchain.mine_block(self.blockchain.hosting_node):
                    print("Mining failed. Got no wallet?")
            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                if Verification.verify_transactions(self.blockchain.get_open_transactions, self.blockchain.get_balance):
                    print("All transactions are valid")
                else:
                    print("There are invalid transactions")
            elif user_choice == "5":
                self.wallet = Wallet()
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == "6":
                pass
                
            elif user_choice == "q":
                waiting_for_input = False
            else:
                print("Input was invalid, please pick a value from the list!")
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("Invalid blockchain!")
                # Break out of the loop
                break
            print("Choice registered!")
            print("Balance of {}: {:6.2f}".format(self.wallet.public_key, self.blockchain.get_balance(self.wallet.public_key)))
        else:
            print("User left!")
                
        print("Done!")
        
if __name__ == "__main__": 
    node = Node()
    node.listen_for_input()
            