#!/bin/sh
#
# Little Tester script

./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --version
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --protocol
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --networkid
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --listening
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --peercount
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --mining
COINBASE=$(./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --coinbase)
echo ${COINBASE}
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --hashrate
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --gasprice
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --accounts
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --blocknumber
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --balance ${COINBASE}
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --txcount ${COINBASE}
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --storage ${COINBASE}
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --blockbyhash 0xeb088bd9560c608aacab338ec24b59623696049ba2baf6d689249bfd9cd06303 

