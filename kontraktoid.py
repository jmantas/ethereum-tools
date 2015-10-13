#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

import eth_rpc
import argparse
import json
from ethereum import _solidity

def main():
#  1000000000000000000 = 1 Ether
   
    
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--host", dest="jrpc_host")
    parser.add_argument("--port", dest="jrpc_port")
    parser.add_argument("--from", dest="from_address",
                        type=str)
    parser.add_argument("--to", dest="to_address",
                        type=str)
    parser.add_argument("--value", dest="value",
                        type=int,
                        default="0")
    parser.add_argument("--gas", dest="gas",
                        type=int, default="90000")
    parser.add_argument("--gasprice", dest="gas_price",
                        type=int,
                        default="50000000000")
    parser.add_argument("--gettxreceipt", dest="tx_hash",
                        type=str)
    parser.add_argument("--getcontractaddress", dest="contract_tx_hash",
                        type=str)
    parser.add_argument("--getcontractcode", dest="contract_address",
                        type=str)
    parser.add_argument("--deploy", dest="contract_code")

    args = parser.parse_args()

    contract_instance = Contract(args.jrpc_host, args.jrpc_port)
    tx_instance = Transaction(args.jrpc_host, args.jrpc_port)

    if args.from_address and args.to_address:
        print tx_instance.tx_send(args.from_address, args.to_address,
            hex(args.gas), hex(args.gas_price), hex(args.value))

    if args.tx_hash:
        print json.dumps(tx_instance.tx_receipt(args.tx_hash), indent=1)

    if args.contract_code:
        with open(args.contract_code) as source_file:
            contract_code = source_file.read()
        contract_byte_code = contract_instance.compile_contract(contract_code)
        print contract_instance.deploy_contract(
            contract_byte_code,
            args.from_address, hex(args.gas),
            hex(args.gas_price))
        
    if args.contract_tx_hash:
        print tx_instance.tx_receipt(args.contract_tx_hash)['contractAddress']
    
    if args.contract_address:
        print contract_instance.contract_code_from_address(args.contract_address)

class Contract(object):
    def __init__(self, rpc_host=None, rpc_port=None):
        self.rpc_host = rpc_host
        self.rpc_port = rpc_port
        self.tx_instance = Transaction(self.rpc_host, self.rpc_port)
        self.eth_instance = eth_rpc.EthRPC(self.rpc_host, self.rpc_port)

    def split_contract(self, contract_code):
        return _solidity.solc_wrapper.split_contracts(contract_code)
    
    def compile_contract(self, contract_code):
        return _solidity.solc_wrapper.compile(contract_code)

    def compile_contract_rich(self, contract_code):
        return _solidity.solc_wrapper.compile_rich(contract_code)

    def deploy_contract(self, contract_byte_code, from_address, gas, gas_price,
                        value=0x0):
        return self.tx_instance.tx_send(
            from_address=from_address,
            gas=gas,
            gas_price=gas_price,
            data='0x{0}'.format(contract_byte_code.encode('hex'))
            )

    def mk_signature(self, contract_code):
        return _solidity.solc_wrapper.mk_full_signature(contract_code)

    def contract_code_from_address(self, contract_address):
        return self.eth_instance.code_from_address_hash(contract_address)


class Transaction(object):
    
    def __init__(self, rpc_host=None, rpc_port=None, from_address=None, 
                to_address=None, gas=None, gas_price=None, value=0x0, 
                data=None, nonce=None, txhash=None):

        self.rpc_host = rpc_host
        self.rpc_port = rpc_port
        self.from_address = from_address
        self.to_address = to_address
        self.gas = gas
        self.gas_price = gas_price
        self.value = value
        self.data = data
        self.nonce = nonce
        self.txhash = txhash
        self.eth_instance = eth_rpc.EthRPC(self.rpc_host, self.rpc_port)
    
    def tx_send(self, from_address=None, to_address=None, 
            gas=None, gas_price=None, value=0x0, data=None, nonce=None):
        return self.eth_instance.send_transaction(
                    from_address=from_address,
                    to_address=to_address,
                    gas=gas,
                    gas_price=gas_price,
                    data=data,
                    value=value
                    )
    
    def tx_receipt(self, txhash):
        return self.eth_instance.transaction_receipt(txhash)


if __name__ == "__main__":
    main()
