#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

''' CLI tool to get basic info from ethereum via JSON-RPC '''

from ethtoollib.eth_rpc import *
from ethtoollib.eth_util import *
import argparse

def main():
    ''' Main function '''
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--host", dest="jrpc_host")
    parser.add_argument("--port", dest="jrpc_port")
    parser.add_argument("--getversion", action="store_true")
    parser.add_argument("--getprotocol", action="store_true")
    parser.add_argument("--getnetworkid", action="store_true")
    parser.add_argument("--islistening", action="store_true")
    parser.add_argument("--getpeercount", action="store_true")
    parser.add_argument("--ismining", action="store_true")
    parser.add_argument("--getcoinbase", action="store_true")
    parser.add_argument("--gethashrate", action="store_true")
    parser.add_argument("--getgasprice", action="store_true")
    parser.add_argument("--getaccounts", action="store_true")
    parser.add_argument("--getblocknumber", action="store_true")
    parser.add_argument("--getbalance", dest="getaccount_balance", type=str)
    parser.add_argument("--gettxcount", dest="getaccount_txcount", type=str)
    parser.add_argument("--getstorage", dest="getaccount_storage", type=str)
    parser.add_argument("--getblockbyhash", dest="getblock_by_hash", type=str)
    parser.add_argument("--getlatestblockinfo", action="store_true")
    parser.add_argument("--getcode", dest="getcode_from_address", type=str)
    args = parser.parse_args()
     
    eth_instance = EthRPC(args.jrpc_host, args.jrpc_port)
     
    if args.getversion:
        print eth_instance.node_version()

    if args.getprotocol:
        print eth_instance.protocol_version()

    if args.getnetworkid:
        print eth_instance.network_id()

    if args.islistening:
        print eth_instance.network_is_listening()

    if args.getpeercount:
        print eth_instance.network_peer_count()

    if args.ismining:
        print eth_instance.node_is_mining()

    if args.getcoinbase:
        print eth_instance.coinbase()

    if args.gethashrate:
        print eth_instance.hashrate()

    if args.getgasprice:
        print eth_instance.gas_price()

    if args.getaccounts:
        accounts_json = eth_instance.accounts()
        print json_to_yamler(accounts_json)

    if args.getblocknumber:
        print eth_instance.current_block_number()

    if args.getaccount_balance:
        acc = args.getaccount_balance
        balance = eth_instance.balance(acc)
        print balance

    if args.getaccount_txcount:
        acc = args.getaccount_txcount
        txcount = eth_instance.transaction_count(acc)
        print txcount

    if args.getaccount_storage:
        acc = args.getaccount_storage
        storage = eth_instance.storage_at(acc)
        print acc, storage

    if args.getblock_by_hash:
        block_hash = args.getblock_by_hash
        info = eth_instance.block_info_by_hash(block_hash)
        print info

    if args.getlatestblockinfo:
        block_number = "latest"
        latestblockinfo_json = eth_instance.block_info_by_number(block_number)
        print json_to_yamler(latestblockinfo_json)
    
    if args.getcode_from_address:
        address = args.getcode_from_address
        info = eth_instance.code_from_address_hash(address)
        print info

if __name__ == "__main__":
    main()
