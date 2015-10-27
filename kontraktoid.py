#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

'''CLI tool to compile and deploy ethereum's contracts.'''

import eth_rpc
import argparse
import json
import ethereum
from ethereum import _solidity
#from ethereum.abi import ContractTranslator, encode_abi, decode_abi
#from ethereum import utils

CONTRACT_BYTE_CODE = None

def main():
    ''' Main function '''
#  1000000000000000000 wei = 1 Ether


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
    parser.add_argument("--getcontractcode", dest="contract_address_code",
                        type=str)
    parser.add_argument("--callcontractaddress", dest="call_contract_address",
                        type=str)
    parser.add_argument("--deploy", dest="deploy_contract")
    parser.add_argument("--abigeth", dest="abi_geth")
    parser.add_argument("--compilecombined", dest="compile_combined")

    args = parser.parse_args()

    contract_instance = Contract(args.jrpc_host, args.jrpc_port)
    tx_instance = Transaction(args.jrpc_host, args.jrpc_port)

    if args.from_address and args.to_address:
        print tx_instance.tx_send(args.from_address, args.to_address,
            hex(args.gas), hex(args.gas_price), hex(args.value))

    if args.tx_hash:
        print json.dumps(tx_instance.tx_receipt(args.tx_hash), indent=1)

    if args.deploy_contract:
        with open(args.deploy_contract) as source_file:
            contract_source_code = source_file.read()
        global CONTRACT_BYTE_CODE
        CONTRACT_BYTE_CODE = contract_instance.compile_contract_eth(contract_source_code)
        print contract_instance.deploy_contract(
            CONTRACT_BYTE_CODE,
            args.from_address, hex(args.gas),
            hex(args.gas_price))

#for testing 
    if args.compile_combined:
        with open(args.compile_combined) as source_file:
            contract_source_code = source_file.read()
        contract_byte_code = contract_instance.compile_contract_combined(contract_source_code)
        print contract_byte_code
#for testing 
        

    if args.abi_geth:
        with open(args.abi_geth) as source_file:
            contract_source_code = source_file.read()
        contract_instance.get_abi_for_geth_console(contract_source_code)


    if args.contract_tx_hash:
        print tx_instance.tx_receipt(args.contract_tx_hash)['contractAddress']

    if args.contract_address_code:
        print contract_instance.contract_code_from_address(args.contract_address_code)

    if args.call_contract_address:
        eth_instance = eth_rpc.EthRPC(args.jrpc_host, args.jrpc_port)
        contract_hex_code = contract_instance.contract_code_from_address(args.call_contract_address)
        print contract_instance.call_contract(
            args.call_contract_address,
            contract_hex_code)



class Contract(object):
    ''' contract object '''
    def __init__(self, rpc_host=None, rpc_port=None):
        self.rpc_host = rpc_host
        self.rpc_port = rpc_port
        self.tx_instance = Transaction(self.rpc_host, self.rpc_port)
        self.eth_instance = eth_rpc.EthRPC(self.rpc_host, self.rpc_port)
        self.contract_byte_code = None
        self.contract_hex_code = None
        self.contract_rich_code = None
        self.contract_code_from_solitidy_rpc = None
        self.contract_combined_code = None
        self.signature = None
        self.translation = None
        self.abi_geth = None

    def translate_contract(self, contract_source_code):
        ''' Method for ContractTranslator '''
        
        ''' mk_signature creates ABI from contracts source code '''
        self.signature = self.mk_signature(contract_source_code)
        self.translation = ContractTranslator(self.signature)
        
        return self.translation 

    def get_abi_for_geth_console(self, contract_source_code):
        ''' gets ABI of mined contract for later use on geth console '''
        
        #self.create_contract(contract_source_code)
        
        ''' mk_signature creates ABI from contracts source code '''
        self.signature = self.mk_signature(contract_source_code)
        ''' replacing some stuff which geth does not like '''
        self.abi_geth = str(self.signature).replace(" ", "").replace("True", "true").replace("False", "false")
        print 'var kontrakt = eth.contract({}).at(\'contractaddresshere\');'.format(self.abi_geth)


    def split_contract(self, contract_code):
        return _solidity.solc_wrapper.split_contracts(contract_code)

    def compile_contract_bin(self, contract_code):
        '''compile with solc binary'''
        pass

    def compile_contract_solidity(self, contract_code):
        '''compile with RPC call'''
        return self.eth_instance.compile_solidity(contract_code)

    def compile_contract_eth(self, contract_code):
        ''' compile with ethereum's module solc_wrapper'''
        return _solidity.solc_wrapper.compile(contract_code)

    def compile_contract_combined(self, contract_code):
        ''' compile with etehreums's module solc_wrapper using
            combined method 
            From source of ethereums module: 
            subprocess.Popen(['solc', '--add-std', '--optimize', '--combined-json', 'abi,bin,devdoc,userdoc'],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        '''
        return _solidity.solc_wrapper.combined(contract_code)

    def compile_contract_rich(self, contract_code):
        ''' compile with ethereum's module solc_wrapper
            get rich output  '''
        return _solidity.solc_wrapper.compile_rich(contract_code)

    def call_contract(self, to_address=None, contract_code=None, default_block="pending"):
        ''' call contract's function_name in to_address. Not tested. '''
        return self.eth_instance.eth_call(to_address, contract_code)

    def deploy_contract(self, contract_byte_code, from_address, gas, gas_price,
                        value=0x0):
        ''' deploy contract by sending compiled byte code '''
        return self.tx_instance.tx_send(
            from_address=from_address,
            gas=gas,
            gas_price=gas_price,
            data='0x{0}'.format(contract_byte_code.encode('hex'))
            )

    def mk_signature(self, contract_code):
        ''' gets ABI with ethereum's module solc_wrapper '''
        return _solidity.solc_wrapper.mk_full_signature(contract_code)

    def contract_code_from_address(self, contract_address):
        ''' gets contract code from address '''
        return self.eth_instance.code_from_address_hash(contract_address)


class Transaction(object):
    ''' transaction object '''
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
        ''' sends transcation '''
        return self.eth_instance.send_transaction(
                    from_address=from_address,
                    to_address=to_address,
                    gas=gas,
                    gas_price=gas_price,
                    data=data,
                    value=value
                    )

    def tx_receipt(self, txhash):
        ''' gets mined transaction receipt '''
        return self.eth_instance.transaction_receipt(txhash)


if __name__ == "__main__":
    main()
