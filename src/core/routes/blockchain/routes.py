# Internal
from utils.converter import list_obj_2_list_dict, obj_2_dict
from blockchain import BlockchainCore
from node import app, request
from transaction import Tx
from block import Block

# TODO: refactor this
obj_types = [type(Block([],'',0)), type(Tx('','',0))]

@app.route('/v1/last_block')
def get_last_block():
    blockchain = BlockchainCore()
    return obj_2_dict(blockchain.get_last_block(), obj_types)


@app.route('/v1/pending_txs')
def get_pending_txs():
    blockchain = BlockchainCore()
    txs = blockchain.get_pending_txs()

    return { 'txs': list_obj_2_list_dict(txs, obj_types) }


@app.route('/v1/tx', methods=['POST'])
def add_tx():
    blockchain = BlockchainCore()

    tx = Tx(
        from_addr=request.json['from_addr'],
        to_addr=request.json['to_addr'],
        amount=request.json['amount']
    )

    tx.sign(request.json['secret'])

    tx_added = blockchain.add_tx(tx)

    return { 'success': tx_added }


@app.route('/v1/blocks')
def get_blocks():
    blockchain = BlockchainCore()

    page = request.args.get('page', default = 1, type = int)
    page_size = request.args.get('page_size', default = 50, type = int)

    blocks, stats = blockchain.get_blocks(page, page_size)

    return { 
        'stats': stats,
        'blocks': list_obj_2_list_dict(blocks, obj_types)
    }

@app.route('/v1/balance')
def get_balance():
    blockchain = BlockchainCore()

    addr = request.args.get('addr', default='', type=str)

    return { 'balance': blockchain.get_balance(addr) }


# TODO: remove this route, and implement third party miner software 
@app.route('/v1/test/mine_block')
def mine_block():
    blockchain = BlockchainCore()

    blockchain.mine_pending_txs('')

    return { 'success': True }

