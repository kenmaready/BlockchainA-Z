This is a simplified blockchain and cryptocurrency network from coding along with Hadelin and Kirill on the "Blockchain A-Z" course on Udemy. The code is somewhat different from the actual course code.

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

In order to create a network among the three, would need to add all nodes to each running server, via a POST request to each server's "/node" path with a json body consisting of a list of the nodes, e.g.:

```
{
  "nodes": [
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",
    "http://127.0.0.1:5003"
  ]
}
```

Once they are updated, conduct some transactions on any of them, using the "/transaction" (POST request with a json object including a "sender", "receiver" and "amount") to add transactions to a particular node, e.g.:

```
{
  "sender": "homer",
  "receiver": "marge",
  "amount": 19.32
}
```

To create a block from a node, hit the "/mine" with simple GET request. Mining a block will automatically add any currently outststanding transactions from that node to the newly mined block. Then can call "/update" (GET request) from each of the nodes to update the ledger across the network. If there are simultaneous blocks being created on different nodes, then the longest chain will win when updating and replace all others upon update. (If there are different chains of equal length, then the first chain of that length reached while polling all the nodes will win.)
