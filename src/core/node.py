# External
from flask import request
from flask import Flask

# Internal
from blockchain import BlockchainCore
from utils.converter import to_json
from transaction import Tx

'''
    TODO: secure the API
        1. Make https
        2. Add validators
        3. Add server error wrapper
'''

blockchain = BlockchainCore()
app = Flask(__name__)


@app.route('/v1/health')
def index():
    return { 'status': 'OK' }


@app.route('/v1/last_block')
def get_last_block():
    return blockchain.get_last_block().to_json()


@app.route('/v1/pending_txs')
def get_pending_txs():
    txs = blockchain.get_pending_txs()

    # temporary shit
    def exc_sign(tx):
        print(tx)
        tx.signature = ''
        return tx

    txs = list(map(exc_sign, txs))

    return to_json(blockchain.get_pending_txs())


@app.route('/v1/tx', methods=['POST'])
def add_tx():
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
  page = request.args.get('page', default = 1, type = int)
  page_size = request.args.get('page_size', default = 1, type = int)
  return to_json(blockchain.get_blocks(page, page_size))