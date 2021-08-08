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
