# External
import requests

# Internal
import configs.miner_constants as miner_constants
from utils.converter import obj_2_dict
from transaction import Tx
from block import Block


# The Miner's software
# It should connect to the blockchain core's miner 
# service. Miners should get/complete challenges 
# via this software.

# Algorithm:
# 1. connect to blockchain
# 2. get pending transactions, previous block hash, difficulty
# 3. form a block
# 4. find nonce
# 5. send to blockchain

addr = miner_constants.ADDR
host = miner_constants.HOST
port = miner_constants.PORT
obj_types = [type(Block([],'',0)), type(Tx('','',0))]

def get_base_url():
    return f"http://{host}:{port}"

def get_txs():
    response = requests.get(url=f"{get_base_url()}/v1/pending_txs")
    json_txs = response.json()['txs']
    return [Tx.read(tx) for tx in json_txs]

def get_previous_block_data():
    response = requests.get(url=f"{get_base_url()}/v1/last_block")
    data = response.json()
    prev_hash = data['hash']
    height = data['height']
    return (prev_hash, height)

def send_block_to_bc(block, miner_addr):
    # data to be sent to api
    data = obj_2_dict(block, obj_types)
    data['miner_addr'] = miner_addr
    
    # sending post request and saving response as response object
    return requests.post(url=f"{get_base_url()}/v1/block", json=data).json()

# Get transactions, previous block's hash and height
txs = get_txs()
prev_hash, height = get_previous_block_data()

# increase height by 1
height = height + 1

new_block = Block(txs, prev_hash, height)
nonce = new_block.mine()

# Output data
print('Txs:', txs)
print('Prev hash:', prev_hash)
print('Height:', height)
print('Nonce:', nonce)
print('\nBlock:', new_block)

# Send to blockchain
print('Send to node:', send_block_to_bc(new_block, addr))