import binascii
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class Wallet:
    def __init(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
        try:
            with open('wallet.txt', mode='w') as f:
                f.write(str(public_key.encode('utf-8')))
                f.write('\n')
                f.write(str(private_key.encode('utf-8')))
        except (IOError, IndexError):
            print("Saving wallet failed!")

    def load_keys(self):
        try:
            with open('wallet.txt', mode='r') as f:
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
            return True
        except (IOError, IndexError):
            print("Loading wallet failed!")
            return False

    def save_keys(self):
        if self.public_key is not None and self.private_key is not None:
            try:
                with open('wallet.txt', mode='w') as f:
                    f.write(str(self.public_key.encode('utf-8')))
                    f.write('\n')
                    f.write(str(self.private_key.encode('utf-8')))
                return True
            except (IOError, IndexError):
                print("Saving wallet failed!")

    def generate_keys(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_key = private_key.public_key()

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return (private_pem.decode('utf-8'), public_pem.decode('utf-8'))

    def sign_transaction(self, sender, recipient, amount):
        private_key = serialization.load_pem_private_key(
            self.private_key.encode('utf-8'),
            password=None
        )
        message = f"{sender}{recipient}{amount}".encode('utf-8')
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return binascii.hexlify(signature).decode('utf-8')

    @staticmethod
    def verify_transaction(transaction):
        public_key = serialization.load_pem_public_key(
            transaction.sender.encode('utf-8')
        )
        try:
            public_key.verify(
                binascii.unhexlify(transaction.signature),
                str(transaction.to_ordered_dict()).encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False


