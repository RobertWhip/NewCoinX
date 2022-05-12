# External
from typing import List, Union

# Internal
from db_models.block_pdb import BlockPDB
from db_models.singleton_meta import SingletonMeta
import configs.constants as constants
import core.configs.errors as errors
from transaction import Tx
from block import Block
from error import Error

'''
    TODO: 
        1. Secure the blockchain
        2. Use a BigNumber lib
        3. Add try-catches
        4. Think about timestamps
'''

class BlockchainCore(metaclass=SingletonMeta):
    def __init__(self) -> None:
        print('Blockchain Core initialized!')
        self.pending_txs = []
        self.db = BlockPDB()
        self.db.init_db(BlockchainCore.get_genesis_blocks())

    def __str__(self) -> str:
        return f'\tBlockchain'

    @staticmethod
    def get_genesis_blocks() -> List[Block]:
        return [
            Block(
                [
                    Tx(
                        constants.DEAD_ADDR, 
                        constants.SATOSHI_ADDR, 
                        constants.INITIAL_AMOUNT
                    ),
                    Tx(
                        constants.SATOSHI_ADDR, 
                        constants.MINER_BUDGET_ADDR, 
                        constants.MINER_BUDGET_AMOUNT
                    )
                ], 
                constants.DEAD_ADDR,
                1
            )
        ]

    def get_last_block(self):
        return self.db.get_last_val()

    def get_max_height(self):
        return self.db.get_last_key()

    def get_blocks(self, page=1, page_size=50):
        max_height = self.get_max_height()

        start = max_height - page * page_size
        stop = max_height - (page - 1) * page_size

        if start < 0:
            start = 0
        if stop > max_height:
            stop = max_height

        it = self.db.open_iter(
            include_start=False,
            include_stop=True,
            include_key=False,
            reverse=True, 
            start=start, 
            stop=stop
        )

        blocks = []
        for val in it:
            blocks.append(self.db.deserialize(val))

        self.db.close_iter(it)

        return blocks, { 'count': max_height, 'pages': -(-max_height//page_size) }

    # Pending txs from memory
    def get_pending_txs(self):
        return self.pending_txs

    # TODO: how to replace this function?
    def mine_pending_txs(self, miner_addr):
        pending_txs = self.get_pending_txs()

        if len(pending_txs) > 0:
            last_block = self.get_last_block()
            block = Block(pending_txs, last_block.hash, last_block.height+1)
            
            block.mine()

            self.db.save([block])

            self.pending_txs = [
                Tx(
                    constants.MINER_BUDGET_ADDR, 
                    miner_addr, 
                    constants.REWARD
                )
            ]

    def add_tx(self, tx: Tx) -> Union[bool, Error]:
        balance = self.get_balance(tx.from_addr)

        is_valid, error = Tx.is_valid(tx, balance)

        if is_valid:
            self.pending_txs.append(tx)
            return True
        else:
            return error

    # TODO: is it a good idea to iterate through all 
    # the blocks just to get the balance? Is there a
    # better solution?
    def get_balance(self, addr):
        balance = 0

        iter = self.db.open_iter(include_key=False)

        for block in iter:
            block = self.db.deserialize(block)

            for tx in block.txs:
                if tx.from_addr == addr:
                    balance = balance - tx.amount
                
                if tx.to_addr == addr:
                    balance = balance + tx.amount

        self.db.close_iter(iter)

        return balance

    def validate(self):
        # TODO: should we validate by a snapshot?
        iter = self.db.open_iter(include_key=False)
        prev_block = self.db.next(iter)

        for val in iter:
            print('Current block: ', val)
            curr_block = self.db.deserialize(val)
            print('Current block: ', curr_block)

            is_curr_block_valid, curr_block_valid_error = Block.is_valid(curr_block)
            if not is_curr_block_valid:
                return curr_block_valid_error

            # If the current block was modified
            if curr_block.hash != curr_block.calc_hash():
                return Error(errors.ERROR_INVALID_BLOCK_HASH)

            # If the current block points to an invalid block
            if curr_block.prev_hash != prev_block.hash:
                return Error(errors.ERROR_INVALID_PREVIOUS_BLOCK_HASH)

            # Set current block as previous block for the next iteration
            prev_block = curr_block

        self.db.close_iter(iter)

        return True

if __name__ == '__main__':
    def create_tx(_from, _to, x, private_key):
        tx = Tx(_from, _to, x)
        tx.sign(private_key)
        return tx

    def add_test_block(blockchain, tx):
        print('Tx created: ', blockchain.add_tx(tx))
        print('Block added')

    privateA, publicA = constants.SATOSHI_SECRET, constants.SATOSHI_ADDR
    privateB, publicB = constants.USER_X_SECRET, constants.USER_X_ADDR
    
    blockchain = BlockchainCore()
    print(blockchain)
    print('Is blockchain valid: ', blockchain.validate())

    add_test_block(blockchain, create_tx(publicA, publicB, 10, privateA))
    
    #add_test_block(blockchain, create_tx(publicB, publicA, 10, privateB))


    blockchain.mine_pending_txs(publicB)

    print(blockchain)
    print('Is blockchain valid: ', blockchain.validate())

    print('\n\nBalance of SATOSHI', blockchain.get_balance(constants.SATOSHI_ADDR))
    print('Balance of USER_X', blockchain.get_balance(constants.USER_X_ADDR))

    blocks = blockchain.get_blocks(1, 9999)
    print('Blocks:\n', blocks)
    for b in blocks:
       print(b)