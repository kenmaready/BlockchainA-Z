# module two - Create a Cryptocurrency

# import libraries:
import requests
from urllib.parse import urlparse
import datetime
import hashlib
import json

# define Jedicoin class:
class Jedicoin:
  @staticmethod
  def block_to_dict(block):
    return {'index': block['index'], 'timestamp': block['timestamp'], 'proof': block['proof'], 'previous_hash': block['previous_hash'], 'transactions': block['transactions']}

  def __init__(self):
    self.chain = []
    self.transactions = []
    self.create_block(proof = 1, previous_hash='0')
    self.nodes = set()

  def create_block(self, proof, previous_hash):
    block = { 'index': len(self.chain) + 1,
              'transactions': self.transactions,
              'timestamp': str(datetime.datetime.now()),
              'proof': proof,
              'previous_hash': previous_hash}
    self.transactions = []
    self.chain.append(block)
    print("Block created: " + str(block['proof']))
    return block
  
  def get_last_block(self):
    return self.chain[-1]

  def proof_of_work(self, previous_proof):
    new_proof = 1
    check_proof = False
    while check_proof is False:
      hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
      if hash_operation[:4] == '0000':
        check_proof = True
      else:
        new_proof += 1
    print("New Proof: " + str(new_proof))
    print("hash_operation: " + hash_operation)

    return new_proof

  def hash(self, block):
    encoded_block = json.dumps(block, sort_keys = True).encode()
    return hashlib.sha256(encoded_block).hexdigest()
  
  def is_chain_valid(self, chain):
    previous_block = chain[0]
    block_index = 1

    while block_index < len(chain):
      block = chain[block_index]
      # 1. Confirm previous hash of current block matches hash
      #    of previous block:
      if block['previous_hash'] != self.hash(previous_block):
        return False

      # 2. Confirm that result of our proofing algorithm for the
      #    two blocks matches the condition (starts with '0000'):
      previous_proof = previous_block['proof']
      current_proof = block['proof']
      hash_operation = hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()
      if hash_operation[:4] != '0000':
        return False

      # iterate our block variables:
      previous_block = block
      block_index += 1

    # if we make it through chain with no 'False' then chain is valid:
    return True

  def add_transaction(self, transaction):
    self.transactions.append({ "sender": transaction['sender'],
                               "receiver": transaction['receiver'],
                               "amount": transaction['amount']})
    previous_block = self.get_last_block()
    return previous_block['index'] + 1
  
  def add_node(self, address):
    parsed_url = urlparse(address)
    self.nodes.add(parsed_url.netloc)
    print("netloc: " + parsed_url.netloc)
  
  def replace_chain(self):
    network = self.nodes
    longest_chain = None
    max_length = len(self.chain)
    for node in network:
      response = requests.get(f'http://{node}/chain')
      if response.status_code == 200:
        length = response.json()['length']
        chain = response.json()['chain']
        if length > max_length and self.is_chain_valid(chain):
            max_length = length
            longest_chain = chain

    if longest_chain:
      self.chain = longest_chain
      return True
    
    return False
