from flask import Flask, jsonify, request
from uuid import uuid4
from Jedicoin import Jedicoin

def create_app(owner):

  app = Flask(__name__)
  app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

  node_address = str(uuid4()).replace('-','')

  coin = Jedicoin()

  @app.route("/mine", methods=['GET'])
  def mine():
    previous_block = coin.get_last_block()
    previous_proof = previous_block["proof"]
    
    proof = coin.proof_of_work(previous_proof)
    previous_hash = coin.hash(previous_block)

    coin.add_transaction({"sender": node_address,
                          "receiver": owner,
                          "amount": 1})

    block = coin.create_block(proof, previous_hash)

    response = { 'message': 'Congratulations, you just mined a block!', **Jedicoin.block_to_dict(block)}

    return jsonify(response), 201


  @app.route("/transaction", methods=['POST'])
  def add_transaction():
    # using a query string to pass transaction parameters:
    # transaction = {}
    # for arg in request.args:
    #   transaction[arg] = request.args[arg]

    # using a json POST to pass transaction parameters
    json = request.get_json()
    transaction_keys = ['sender','receiver','amount']

    if not all (key in json for key in transaction_keys):
      return jsonify({ "error": True, "message": "Invalid transaction submission (must include sender, receiver and amount)."}), 400

    index = coin.add_transaction(json)

    if index == -1:
        return jsonify({ "error": True, "message": "Something went wrong. Transaction not posted."})
    
    return jsonify({ "success": True, "message": f"Transaction will be added to block {index}." }), 200


  @app.route("/chain", methods=['GET'])
  def get_chain():
    response = {'chain': coin.chain, 'length': len(coin.chain) }
    return jsonify(response), 200



  @app.route("/validate", methods=['GET'])
  def validate_chain():
    response = { 'validated': coin.is_chain_valid(coin.chain)}
    return jsonify(response), 200


  @app.route("/node", methods=['POST'])
  def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')

    if nodes is None:
      return jsonify({"error": True, "message": "Invalid request. Must include node identifier."}), 400
    
    for node in nodes:
      coin.add_node(node)
    
    return jsonify({"succes": True, "message": "New node has been added.", "nodes": list(coin.nodes)}), 201


  @app.route("/update", methods=['GET'])
  def update_chain():
    chain_updated = coin.replace_chain()

    if chain_updated:
      message = "Chain has been updated on this node."
    else:
      message = "This node's chain was already up to date."
    
    return jsonify({ "success": True, "message": message, "chain": coin.chain }), 200

  return app

def launch_app(owner, port):
  app = create_app(owner)
  app.run(host = '0.0.0.0', port=port)