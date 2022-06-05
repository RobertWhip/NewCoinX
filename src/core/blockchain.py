# External
from typing import List, Union
import copy

# Internal
from db_models.singleton_meta import SingletonMeta
from db_models.block_pdb import BlockPDB
import configs.constants as constants
import core.configs.errors as errors
from transaction import Tx
from block import Block
from error import Error

class BlockchainCore(metaclass=SingletonMeta):
    # Init blockchain
    def __init__(self) -> None:
        self.pending_txs: List[Tx] = []
        self.db: BlockPDB = BlockPDB()

        # Create DB with genesis block if it wasn't yet
        self.db.init_db(BlockchainCore.get_genesis_blocks())

        # TODO: add more flexible logger
        print('Blockchain Core initialized!')

    def __str__(self) -> str:
        return f'\tBlockchain'

    # Get genesis block (first block of blockchain)
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

    # Get last block of blockchain
    def get_last_block(self):
        return self.db.get_last_val()

    # Get latest height (height of the latest block)
    def get_max_height(self):
        return self.db.get_last_key()

    # Get a list of blocks
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

    # Get pending transactions
    def get_pending_txs(self):
        return copy.deepcopy(self.pending_txs)

    # Add block to blockchain
    def add_block(self, block_dict, miner_addr):
        block = Block.read(block_dict)
        # check if the miner mined pending txs
        mined_txs = []

        for tx in block.txs:
            for p_tx in self.pending_txs:
                if tx.hash == p_tx.hash:
                    mined_txs.append(p_tx.hash)

        if len(mined_txs) != len(block.txs):
            return {
                'success': False,
                'msg': str(Error(errors.ERROR_INVALID_TXS))
            }

        # validate blockchain with new block
        validated, error = self.validate(block)
        if not validated:
            return {
                'success': False,
                'msg': str(error)
            }

        # At this moment the block fully validated by this node.
        # Now we remove the mined transactions from pending ones.
        for tx_hash in mined_txs:
            for i in range(len(self.pending_txs)-1, -1, -1):
                if tx_hash == self.pending_txs[i].hash:
                    del self.pending_txs[i]

        self.db.save([block])

        if miner_addr:
            self.pending_txs.append(
                Tx(
                    constants.MINER_BUDGET_ADDR, 
                    miner_addr, 
                    constants.REWARD
                )
            )

        return { 'success': True }

    # Add a pending transaction
    def add_tx(self, tx: Tx) -> Union[bool, Error]:
        balance = self.get_balance(tx.from_addr)

        is_valid, error = Tx.is_valid(tx, balance)

        if is_valid:
            self.pending_txs.append(tx)
            return True
        else:
            return error

    # Get balance of an address
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

    # Validate two blocks
    def __validate_pair(self, curr_block, prev_block):
        is_curr_block_valid, curr_block_valid_error = Block.is_valid(curr_block)
        if not is_curr_block_valid:
            return False, curr_block_valid_error

        # If the current block was modified
        if curr_block.hash != curr_block.calc_hash():
            return False, Error(errors.ERROR_INVALID_BLOCK_HASH)

        # If the current block points to an invalid block
        if curr_block.prev_hash != prev_block.hash:
            return False, Error(errors.ERROR_INVALID_PREVIOUS_BLOCK_HASH)

        return True, None

    # Validate blockchain
    def validate(self, new_block:Block=None):
        iter = self.db.open_iter(include_key=False)
        prev_block = self.db.next(iter)

        for val in iter:
            curr_block = self.db.deserialize(val)

            block_validated, block_error = self.__validate_pair(curr_block, prev_block)
            if not block_validated:
                return False, block_error

            # Set current block as previous block for the next iteration
            prev_block = curr_block

        # All blocks are validated at this step.

        # Now validate the that we wan't to add
        # if it is given as a function argument.
        if new_block:
            block_validated, block_error = self.__validate_pair(new_block, prev_block)
            if not block_validated:
                return False, block_error


        # Close DB iterator
        self.db.close_iter(iter)

        # Verified, no errors
        return True, None

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
    print('Is blockchain valid: ', blockchain.validate())

    add_test_block(blockchain, create_tx(publicA, publicB, 10, privateA))
    
    blockchain.mine_pending_txs(publicB)

    print('Is blockchain valid: ', blockchain.validate())

    print('\n\nBalance of SATOSHI', blockchain.get_balance(constants.SATOSHI_ADDR))
    print('Balance of USER_X', blockchain.get_balance(constants.USER_X_ADDR))

    blocks, stats = blockchain.get_blocks(1, 9999)
    print('Blocks:\n', blocks)
    
    for b in blocks:
       print(b)
