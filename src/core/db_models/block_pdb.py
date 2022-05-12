# External
from typing import List
import sys

sys.path.append('..')

# Internal
import configs.constants as constants
import configs.db as db_configs
from transaction import Tx
from block import Block
from db_models.db import DBModel


class BlockPDB(DBModel):
    def __init__(self, prefix='') -> None:
        super().__init__(prefix + db_configs.DB_BX_PREFIX)

    # Basically this function supposed to create the genesis block 
    # when it was not initiated locally yet.
    def init_db(self, blocks) -> bool:
        is_init = self.superdb_get(db_configs.INIT_KEY)

        if not is_init:
            self.save(blocks)
            self.superdb_put(db_configs.INIT_KEY, True)

        return is_init

    # Save blocks
    #
    # This function will save the given blocks in local LevelDB.
    # Key = the block's height, value = the block itself
    #
    # return True if succeed
    def save(self, blocks: List[Block]) -> bool:
        super().save(blocks, lambda bx: bx.height)
        return True


if __name__ == '__main__':
    print('Test prefixed block db.\n')

    '''

    # create prefixed database
    block_pdb = BlockPDB('test_')


    # save some blocks
    txs0 = [
        Tx(constants.SATOSHI_ADDR, constants.USER_X_ADDR, 200),
        Tx(constants.USER_X_ADDR, constants.SATOSHI_ADDR, 100)
    ]
    txs1 = [
        Tx(constants.SATOSHI_ADDR, constants.USER_X_ADDR, 500),
        Tx(constants.USER_X_ADDR, constants.SATOSHI_ADDR, 500),
        Tx(constants.DEAD_ADDR, constants.MINER_BUDGET_ADDR, 500)
    ]
    blocks = [
        Block(txs0, 'f59dc0ec9502931b311a6c96eb95aeed072f5f6127f414dd05cb9c111353e179', 23),
        Block(txs1, 'fe32baa8b37661dcac0e7d610679e35c989d152d91343e57865fefae81372247', 3)
    ]
    #block_pdb.save(blocks)

    # output blocks
    it = block_pdb.open_iter(
        # start='9e008c5b7a12422542f38ea6252e7dfc252a59d5b6b8d32f8e2d1faa02b1cbd7',
        # stop='fe32baa8b37661dcac0e7d610679e35c989d152d91343e57865fefae81372247',
        # snapshot=True
    )

    for key, val in it:
        print(
            block_pdb.deserialize(key), '\n',
            block_pdb.deserialize(val)
        )

        #print(block_pdb.deserialize(val).txs[1])

    block_pdb.close_iter(it)


    # Example 2
    # Iterate through the blocks and compare 
    # current and previous blocks.
    iter = block_pdb.open_iter(include_value=False)
    prev = block_pdb.next(iter)

    for key in iter:
        key = block_pdb.deserialize(key)

        print(prev, key) # compare
        prev = key

    block_pdb.close_iter(iter)


    # Example 3
    # get last block and key
    last_bl = block_pdb.get_last_val()
    print(last_bl)

    last_key = block_pdb.get_last_key()
    print(last_key)

    '''
    # is singleton

    s1 = BlockPDB()
    s2 = BlockPDB()

    print(s1.get_last_key())
    print(s2.get_last_key())

    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")