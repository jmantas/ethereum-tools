#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

''' eth rpc module'''

import json
import requests

class EthRPC(object):
    ''' eth connection initialization '''
    json_id = 0

    def __init__(self, host=None, port=None):
        self.json_rpc_host = host
        self.json_rpc_port = port
        self.scheme = 'http'
        self.session = requests.session()

    def json_id_index(self):
        ''' Iterator '''
        self.json_id += 1
        return self.json_id

    def init_rpc_request(self, rpc_method, json_parameters=None):
        ''' JSON-RPC connector '''
        json_data = json.dumps({
            "jsonrpc": "2.0",
            "method": rpc_method,
            "params": json_parameters,
            "id": self.json_id_index(),
            })
        url = '{http}://{host}:{port}/'.format(
            http=self.scheme,
            host=self.json_rpc_host,
            port=self.json_rpc_port
            )
        json_output = self.session.post(url, data=json_data).json()
        if json_output and 'error' in json_output:
            raise ValueError(json_output)
        return json_output


    def node_version(self):
        ''' get node version '''
        rpc_request_output = self.init_rpc_request(
            "web3_clientVersion")
        return rpc_request_output['result']

    def protocol_version(self):
        ''' get protocol version '''
        rpc_request_output = self.init_rpc_request(
            "eth_protocolVersion")
        return rpc_request_output['result']

    def network_id(self):
        ''' get network ID '''
        rpc_request_output = self.init_rpc_request(
            "net_version")
        return rpc_request_output['result']

    def network_is_listening(self):
        ''' listen status '''
        rpc_request_output = self.init_rpc_request(
            "net_listening")
        return rpc_request_output['result']

    def network_peer_count(self):
        ''' get peer count '''
        rpc_request_output = self.init_rpc_request(
            "net_peerCount")
        return int(rpc_request_output['result'], 16)

    def blockchain_syncing(self):
        ''' gets blockchains sync status '''
        rpc_request_output = self.init_rpc_request("eth_isSyncing")
        return rpc_request_output['result']


    def node_is_mining(self):
        ''' mining status '''
        rpc_request_output = self.init_rpc_request(
            "eth_mining")
        return rpc_request_output['result']

    def coinbase(self):
        ''' get coinbase '''
        rpc_request_output = self.init_rpc_request(
            "eth_coinbase")
        return rpc_request_output['result']

    def hashrate(self):
        ''' get hasrate '''
        rpc_request_output = self.init_rpc_request(
            "eth_hashrate")
        return int(rpc_request_output['result'], 16)

    def gas_price(self):
        ''' get gas price '''
        rpc_request_output = self.init_rpc_request(
            "eth_gasPrice")
        return int(rpc_request_output['result'], 16)

    def accounts(self):
        ''' get list of accounts '''
        rpc_request_output = self.init_rpc_request(
            "eth_accounts")
        return rpc_request_output['result']

    def current_block_number(self):
        ''' get latest block number '''
        rpc_request_output = self.init_rpc_request(
            "eth_blockNumber")
        return int(rpc_request_output['result'], 16)

    def balance(self, account, block_number="latest"):
        ''' get balance for account hash,
            by default at latest synced block number '''
        rpc_request_output = self.init_rpc_request(
            "eth_getBalance", [account, block_number])
        return int(rpc_request_output['result'], 16)

    def transaction_count(self, account, block_number="latest"):
        ''' get transaction count for account hash '''
        rpc_request_output = self.init_rpc_request(
            "eth_getTransactionCount", [account, block_number])
        return int(rpc_request_output['result'], 16)

    def storage_at(self, account, position="0x0", block_number="latest"):
        ''' returns storage at account latest block in position 0x0 '''
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


    def sign_data(self, address, data):
        rpc_request_output = self.init_rpc_request("eth_sign",
                                                    [address, data])
        return rpc_request_output['result']

    def send_transaction(self, from_address=None, to_address=None, gas=None,
                        gas_price=None, value=None, data=None, nonce=None):
        ''' send transaction '''
        transaction_params = {
                'from':     from_address,
                'to':       to_address if to_address else None,
                'gas':      gas,
                'gasPrice': gas_price,
                'value':    value if value else None,
                'data':     data if data else None
        }
        rpc_request_output = self.init_rpc_request(
            "eth_sendTransaction", [transaction_params])
        return rpc_request_output['result']


    def transaction_receipt(self, transaction_hash):
        rpc_request_output = self.init_rpc_request(
            "eth_getTransactionReceipt", [transaction_hash])
        return rpc_request_output['result']


    def eth_call(self, from_address=None, to_address=None, gas=None, gas_price=None, value=None, data=None):
        ''' calls contract '''
        transaction_params = {
                'from':     from_address,
                'to':       to_address if to_address else None,
                'gas':      gas,
                'gasPrice': gas_price,
                'value':    value if value else None,
                'data':     data if data else None
        }

        rpc_request_output = self.init_rpc_request(
            "eth_call", [transaction_params])
        return rpc_request_output['result']

# eth_sendRawTransaction


    def eth_estimate_gas(self, from_address=None, to_address=None,
                        gas=None, gas_price=None, value=None, data=None):
        ''' estimates gas per transaction by creating dummy tx which does
            not get into blockchain '''
        transaction_params = {
                'from':     from_address if from_address else None,
                'to':       to_address if to_address else None,
                'gas':      gas if gas else None,
                'gasPrice': gas_price if gas_price else None,
                'value':    value if value else None,
                'data':     data if data else None
        }

        rpc_request_output = self.init_rpc_request(
            "eth_estimateGas", [transaction_params])
        return rpc_request_output['result']



    def compile_solidity(self, contract_source_code):
        rpc_request_output = self.init_rpc_request(
            "eth_compileSolidity", [contract_source_code])
        return rpc_request_output['result']

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

