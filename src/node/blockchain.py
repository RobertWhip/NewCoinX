import sys
sys.path.append('..')

from block import Block
from configs import constants 
from transaction import Tx
import configs.constants as constants


class Blockchain:
    def __init__(self) -> None:
        self.blocks = [Blockchain.get_source_block()]

    def __str__(self) -> str:
        return f' Blockchain:\n\
            Blocks: {[block.hash for block in self.blocks]}'

    @staticmethod
    def get_source_block():
        return Block(
            0, 
            [
                Tx(
                    constants.DEAD_ADDR, 
                    constants.SATOSHI_ADDR, 
                    constants.INITIAL_AMOUNT
                )
            ], 
            constants.DEAD_ADDR
        )

    def add_block(self, block):
        self.blocks.append(block)


if __name__ == '__main__':
    blockchain = Blockchain()
    print(blockchain)

    txs = [Tx('a', 'b', 5), Tx('a', 'b', 5), Tx('a', 'b', 5)]
    block = Block(0, txs, '0')

    blockchain.add_block(block)
    print(blockchain)