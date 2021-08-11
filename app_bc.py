from flask import Flask, jsonify
from Blockchain import Blockchain


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


bc = Blockchain()

@app.route("/mine", methods=['GET'])
def mine():
  previous_block = bc.get_last_block()
  previous_proof = previous_block["proof"]
  
  proof = bc.proof_of_work(previous_proof)
  previous_hash = bc.hash(previous_block)

  block = bc.create_block(proof, previous_hash)

  response = { 'message': 'Congratulations, you just mined a block!', **Blockchain.block_to_dict(block)}

  return jsonify(response), 201



@app.route("/chain", methods=['GET'])
def get_chain():
  response = {'chain': bc.chain, 'length': len(bc.chain) }
  return jsonify(response), 201



@app.route("/validate", methods=['GET'])
def validate_chain():
  response = { 'validated': bc.is_chain_valid(bc.chain)}
  return jsonify(response), 200

app.run(host = '0.0.0.0', port='5000')