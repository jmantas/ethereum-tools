#!/bin/sh
#
# Little Tester script

./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getversion
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getprotocol
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getnetworkid
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --islistening
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getpeercount
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --ismining
COINBASE=$(./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getcoinbase)
echo ${COINBASE}
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --gethashrate
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getgasprice
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getaccounts
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getblocknumber
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getbalance ${COINBASE}
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --gettxcount ${COINBASE}
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getstorage ${COINBASE}
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getblockbyhash 0xeb088bd9560c608aacab338ec24b59623696049ba2baf6d689249bfd9cd06303 

./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getlatestblockinfo
./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --getcode 0x11e18ab77f6ca65a3aa5e7172ee86612ca301053
