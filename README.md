The "main" file is the entry point. Run from command line:

```
pipenv run main
```

There are three separate main files (main.py, main2.py and main3.py) to allow you to set up three "nodes" or users on the crypto network, and update each other's chains (the current ledger). This just tolls the chains of the other nodes and if there is a longer chain somewhere on the network, it will update the current node. It is a 'pull' operation, so you would have to send a GET request to '/update' in order to initiate.

In order to run the three nodes and test the networking/distributed functionality, run these commands from different terminals:

```
pipenv run main
pipenv run main2
pipenv run main3
```

In order to create a network among the three, would need to add all nodes to each running server, via a POST request to each server with a json body consisting of a list of the nodes, e.g.:

```
{
  "nodes": [
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",
    "http://127.0.0.1:5003"
  ]
}
```

Once they are updated, conduct some transactions on any of them, using the "/transaction" (POST request with a json object including a "sender", "receiver" and "amount") to add transactions to a particular node, and then "/mine" (GET request) that node in order to mine a new block and add the pool of transactions to the blockchain. Then can call "/update" (GET request) from each of the nodes to update the ledger across the network.
