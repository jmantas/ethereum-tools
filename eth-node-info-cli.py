#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

''' CLI tool to get basic info from ethereum via JSON-RPC '''

import json
import requests
import argparse


def main():
    ''' Main function '''
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--host", dest="jrpc_host")
    parser.add_argument("--port", dest="jrpc_port")
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--protocol", action="store_true")
    parser.add_argument("--networkid", action="store_true")
    parser.add_argument("--listening", action="store_true")
    parser.add_argument("--peercount", action="store_true")
    parser.add_argument("--mining", action="store_true")
    parser.add_argument("--coinbase", action="store_true")
    parser.add_argument("--hashrate", action="store_true")
    parser.add_argument("--gasprice", action="store_true")
    parser.add_argument("--accounts", action="store_true")
    parser.add_argument("--blocknumber", action="store_true")
    parser.add_argument("--balance", dest="account_balance", type=str)
    parser.add_argument("--txcount", dest="account_txcount", type=str)
    args = parser.parse_args()

    eth_instance = EthClient(args.jrpc_host, args.jrpc_port)

    if args.version:
        print "Node version:{}".format(eth_instance.node_version())

    if args.protocol:
        print "Protocol version:{}".format(eth_instance.protocol_version())

    if args.networkid:
        print "Network ID:{}".format(eth_instance.network_id())

    if args.listening:
        print "Nerwork listening:{}".format(eth_instance.network_is_listening())

    if args.peercount:
        print "Peer count:{}".format(eth_instance.network_peer_count())

    if args.mining:
        print "Node mining:{}".format(eth_instance.node_is_mining())

    if args.coinbase:
        print "Coinbase:{}".format(eth_instance.coinbase())

    if args.hashrate:
        print "Hashrate:{}".format(eth_instance.hashrate())

    if args.gasprice:
        print "Gasprice:{}".format(eth_instance.gas_price())

    if args.accounts:
        print "Accounts:{}".format(eth_instance.accounts())

    if args.blocknumber:
        print "Last block number:{}".format(eth_instance.current_block_number())

    if args.account_balance:
        acc = args.account_balance
        balance = eth_instance.balance(acc)
        print "Balance for {} is:{}".format(acc, balance)

    if args.account_txcount:
        acc = args.account_txcount
        txcount = eth_instance.transaction_count(acc)
        print "Transaction count for {} is:{}".format(acc, txcount)

class EthClient(object):
    ''' eth connection initialization '''
    json_id = 0

    def __init__(self, host, port):
        self.json_rpc_host = host
        self.json_rpc_port = port
        self.session = requests.session()

    def json_id_index(self):
        ''' Iterator '''
        self.json_id += 1
        return self.json_id

    def init_rpc_request(self, rpc_method, json_parameters):
        ''' JSON-RPC connector '''
        json_data = self.session.post('http://{host}:{port}/'.format
        (host=self.json_rpc_host, port=self.json_rpc_port),
        data=json.dumps({
            "jsonrpc": "2.0",
            "method": rpc_method,
            "params": json_parameters,
            "id": self.json_id_index(),
            })
        )
        json_output = json_data.json()
        if json_output and 'error' in json_output:
            raise ValueError(json_output)
        return json_output


    def node_version(self):
        ''' get node version '''
        rpc_request_output = self.init_rpc_request(
            "web3_clientVersion", [])
        return rpc_request_output['result']

    def protocol_version(self):
        ''' get protocol version '''
        rpc_request_output = self.init_rpc_request(
            "eth_protocolVersion", [])
        return rpc_request_output['result']

    def network_id(self):
        ''' get network ID '''
        rpc_request_output = self.init_rpc_request(
            "net_version", [])
        return rpc_request_output['result']

    def network_is_listening(self):
        ''' listen status '''
        rpc_request_output = self.init_rpc_request(
            "net_listening", [])
        return rpc_request_output['result']

    def network_peer_count(self):
        ''' get peer count '''
        rpc_request_output = self.init_rpc_request(
            "net_peerCount", [])
        return int(rpc_request_output['result'], 16)

#ValueError: {u'jsonrpc': u'2.0', u'id': 999, u'error': {u'message': u'eth_isSyncing method not implemented', u'code': -32601}}
#    def blockchain_syncing(self):
#        rpc_request_output = self.init_rpc_request("eth_isSyncing", [])
#        return rpc_request_output['result']


    def node_is_mining(self):
        ''' mining status '''
        rpc_request_output = self.init_rpc_request(
            "eth_mining", [])
        return rpc_request_output['result']

    def coinbase(self):
        ''' get coinbase '''
        rpc_request_output = self.init_rpc_request(
            "eth_coinbase", [])
        return rpc_request_output['result']

    def hashrate(self):
        ''' get hasrate '''
        rpc_request_output = self.init_rpc_request(
            "eth_hashrate", [])
        return int(rpc_request_output['result'], 16)

    def gas_price(self):
        ''' get gas price '''
        rpc_request_output = self.init_rpc_request(
            "eth_gasPrice", [])
        return int(rpc_request_output['result'], 16)

    def accounts(self):
        ''' get list of accounts '''
        rpc_request_output = self.init_rpc_request(
            "eth_accounts", [])
        return rpc_request_output['result']

    def current_block_number(self):
        ''' get latest block number '''
        rpc_request_output = self.init_rpc_request(
            "eth_blockNumber", [])
        return int(rpc_request_output['result'], 16)

    def balance(self, account, block_number="latest"):
        ''' get balance for account hash, by default at latest synced block number '''
        rpc_request_output = self.init_rpc_request(
            "eth_getBalance", [account, block_number])
        return int(rpc_request_output['result'], 16)

    def transaction_count(self, account, block_number="latest"):
        ''' get transaction count for account hash '''
        rpc_request_output = self.init_rpc_request(
            "eth_getTransactionCount", [account, block_number])
        return int(rpc_request_output['result'], 16)





    def storage_at(self, account, position="0x0", block_number="latest"):
        rpc_request_output = self.init_rpc_request(
            "eth_getStorageAt", [account, position, block_number])
        return rpc_request_output['result']

    def transaction_count_in_block(self, block_hash):
        rpc_request_output = self.init_rpc_request(
            "eth_getBlockTransactionCountByHash", [block_hash])
        return int(rpc_request_output['result'], 16)

    def uncle_count_from_block_hash(self, block_hash):
        rpc_request_output = self.init_rpc_request(
            "eth_getUncleCountByBlockHash", [block_hash])
        return int(rpc_request_output['result'], 16)

    def uncle_count_from_block_number(self, block_number):
        rpc_request_output = self.init_rpc_request(
            "eth_getUncleCountByBlockNumber", [block_number])

        return int(rpc_request_output['result'], 16)

    def code_from_address_hash(self, address, block_number="latest"):
        rpc_request_output = self.init_rpc_request(
            "eth_getCode", [address, block_number])
        return rpc_request_output['result']


#    how to unlock with RPC?? not working when unlocked in geth console
#    def sign_data(self, address, data):
#        rpc_request_output = self.init_rpc_request("eth_sign",
#                                                    [address, data])
#        return rpc_request_output['result']

# eth_sendTransaction
# eth_sendRawTransaction
# eth_call
# eth_estimateGas


    def block_info_by_hash(self, block_hash, full_bool=True):
        rpc_request_output = self.init_rpc_request(
            "eth_getBlockByHash", [block_hash, full_bool])
        return rpc_request_output['result']

    def block_info_by_number(self, block_number, full_bool=True):
        rpc_request_output = self.init_rpc_request(
            "eth_getBlockByNumber", [block_number, full_bool])
        return rpc_request_output['result']


    def transaction_info_by_hash(self, transaction_hash):
        rpc_request_output = self.init_rpc_request(
            "eth_getTransactionByHash", [transaction_hash])
        return rpc_request_output['result']

#eth_getTransactionByBlockHashAndIndex



if __name__ == "__main__":
    main()
