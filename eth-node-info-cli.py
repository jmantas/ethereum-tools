#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

''' CLI tool to get basic info from ethereum via JSON-RPC '''

import eth_rpc
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
    parser.add_argument("--storage", dest="account_storage", type=str)
    parser.add_argument("--blockbyhash", dest="block_by_hash", type=str)
    args = parser.parse_args()

    
    eth_instance = eth_rpc.EthRPC(args.jrpc_host, args.jrpc_port)

    if args.version:
        print eth_instance.node_version()

    if args.protocol:
        print eth_instance.protocol_version()

    if args.networkid:
        print eth_instance.network_id()

    if args.listening:
        print eth_instance.network_is_listening()

    if args.peercount:
        print eth_instance.network_peer_count()

    if args.mining:
        print eth_instance.node_is_mining()

    if args.coinbase:
        print eth_instance.coinbase()

    if args.hashrate:
        print eth_instance.hashrate()

    if args.gasprice:
        print eth_instance.gas_price()

    if args.accounts:
        print eth_instance.accounts()

    if args.blocknumber:
        print eth_instance.current_block_number()

    if args.account_balance:
        acc = args.account_balance
        balance = eth_instance.balance(acc)
        print balance

    if args.account_txcount:
        acc = args.account_txcount
        txcount = eth_instance.transaction_count(acc)
        print txcount

    if args.account_storage:
        acc = args.account_storage
        storage = eth_instance.storage_at(acc)
        print acc, storage


    if args.block_by_hash:
        block_hash = args.block_by_hash
        info = eth_instance.block_info_by_hash(block_hash)
        print info


if __name__ == "__main__":
    main()
