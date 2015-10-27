#!/bin/sh
#
# Little Tester script

#contract deployment
echo "Deploying contract..."
TXHASH=`./kontraktoid.py --host 127.0.0.1 --port 18801 --gas 3000000 --from "0x6a60fd076328f75a03c5a289ddbf68f125ebc4ee" --deploy $1`
echo "Trasaction hash of the deployed contract:"
echo ${TXHASH}

# get contract call ABI and address formated for copypasting intho geth console
# for testing simple solidity contracts
echo "Getting contract ABI..."
ABI=`./kontraktoid.py --host 127.0.0.1 --port 18801 --abigeth $1`

# get status of mining, if truewait for ~60 sec for block to mine
MINING_BOOL=`./eth-node-info-cli.py --host 127.0.0.1 --port 18801 --mining`

if test "${MINING_BOOL}" = "True"
#if [ "{$MINING_BOOL}" == "True" ] 
then
        echo "waiting for ~60 sec, for block to be mined. Probably ... for sure ..."
        sleep 60
    else
        echo "Not mining"
        exit 1
fi

#get contract address from deployed transaction hash
ADDRESS=`./kontraktoid.py --host 127.0.0.1 --port 18801 --getcontractaddress ${TXHASH}`

#get contract code from address
CODE=`./kontraktoid.py --host 127.0.0.1 --port 18801 --getcontractcode ${ADDRESS}`


echo "variable on geth console for contracts functions call:"
echo ${ABI} | sed -e "s/contractaddresshere/${ADDRESS}/g"

echo "Address of the contract:"
echo ${ADDRESS}

echo "Code of the contract:"
echo ${CODE}

