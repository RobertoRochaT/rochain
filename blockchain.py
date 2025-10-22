import hashlib
import json

from time import time
from uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis ( a block with no predecessors )
        self.new_block(previous_hash = 1, proof=100)

    def proof_of_work(self,last_proof):
        """
            Simple Proof of work algorithm:
                - Find a number p' such that hash(pp') contains leading 4 zeroes,
                  where p is the previous

                - p is the previous proof, and p' is the new proof
            :param last_proof: <int>
            :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof,proof) is False:
            proof +=1
        return proof
    
    def new_block(self,proof,previous_hash = None):
        """
            Create a new Block in the BlockChain
            :param proof: <int> The proof given by the Proof of Work algorithm
            :param previous_hash (Optional) <str> Hash of the previous Block
            :return <dic> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self,sender,recipient,amount):
        """
            Creates a new transaction to go into the next mined block
            :param sender: <str> Address of the sender
            :param recipient: <str> Address of the recipient
            :param amount: <int> Amount
            :return <int> The index of the block that will hold this transaction
        """
        self.current_transactions.append({
            'sender' : sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1
    @staticmethod
    def valid_proof(last_proof, proof):
        """
            Validates the proof: Does hash(last,proof) contains 4 leading zeroes?
            :param last_proof: <int> Previous Proof
            :param proof: <int> Current Proof
            :return: <bool> True if correct, False if not
        """
        guess = f'{last_proof}{proof}'
        guess_hash = hashlib.sha256(guess.encode()).hexdigest()
        return guess_hash[:4] == '0000'

    @staticmethod
    def hash(block):
        """
            Creates a SHA-256 hash of Block
            :param block: <dict> Block
            :return <str>
        """

        # We must make sure that the Dictionary is Ordered, or we´ll have inconsistent hashes
        block_string = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

