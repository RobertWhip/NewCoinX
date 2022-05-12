# External
from typing import List, overload
import sys

sys.path.append('..')

# Internal
import configs.constants as constants
import configs.db as db_configs
from transaction import Tx
from db import DBModel

# TODO: do we need this model?
# Should we store blocks and transactions separately?
# Or should we store them together?

# !!! This class was not propely tested. DO NOT USE IT

class TransactionPDB(DBModel):
    def __init__(self, prefix='') -> None:
        super().__init__(prefix + db_configs.DB_TX_PREFIX)

    def save(self, txs: List[Tx]) -> bool:
        super().save(txs)


if __name__ == '__main__':
    print('Test transaction prefixed db.\n')

    # create prefixed database
    tx_pdb = TransactionPDB('test_')

    # save some transactions
    txs = [
        Tx(constants.SATOSHI_ADDR, constants.USER_X_ADDR, 500),
        Tx(constants.USER_X_ADDR, constants.SATOSHI_ADDR, 500),
        Tx(constants.DEAD_ADDR, constants.MINER_BUDGET_ADDR, 500)
    ]
    tx_pdb.save(txs)

    # output transactions
    it = tx_pdb.open_iter(
        # start='f59dc0ec9502931b311a6c96eb95aeed072f5f6127f414dd05cb9c111353e179',
        # stop='fe32baa8b37661dcac0e7d610679e35c989d152d91343e57865fefae81372247',
        # snapshot=True
    )

    for key, val in it:
        print(
            tx_pdb.deserialize(key), '\n',
            tx_pdb.deserialize(val)
        )


    tx_pdb.close_iter(it)