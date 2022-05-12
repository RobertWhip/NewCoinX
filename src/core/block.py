# External
from typing import Tuple
from typing import List
import hashlib
import json
import sys
sys.path.append('..')

# Internal
import configs.constants as constants
import configs.errors as errors
from transaction import Tx
from error import Error
import utils.timestamp as timestamp


class Block:
    def __init__(
        self,
        txs: List[Tx],
        prev_hash: str,
        height: int
    ) -> None:
        self.txs: List[Tx] = txs
        self.prev_hash: str = prev_hash
        self.height: int = height
        self.timestamp = timestamp.now()
        self.nonce: int = 0
        self.version = 0
        self.hash: str = self.calc_hash()


    def __str__(self) -> str:
        return f'\tBlock:\n\
            Hash: {self.hash}\n\
            Previous hash: {self.prev_hash}\n\
            Height: {self.height}\n\
            Nonce: {self.nonce}\n\
            Version: {self.version}\n\
            Timestamp: {self.timestamp}\n\
            TXs: {[tx.hash for tx in self.txs]}\n'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def calc_hash(self) -> str:
        return hashlib.sha256(
            (
                ''.join([tx.hash for tx in self.txs]) + 
                self.prev_hash +
                str(self.height) +
                str(self.timestamp) +
                str(self.nonce)
            ).encode('utf-8')
        ).hexdigest()

    @staticmethod
    def verify_txs(block) -> tuple([bool, Error]):
        print('Block in verify txs:', block)

        if block.txs is None or len(block.txs) <= 0:
            return False, Error(errors.ERROR_TRANSACTIONS_NOT_FOUND)

        for tx in block.txs:
            is_tx_valid, tx_error = Tx.is_valid(tx, None)

            if not is_tx_valid:
                return False, tx_error

        return True, None

    @staticmethod
    def is_valid(block) -> bool:
        print('Is block valid\'s block: ', block)
        return Block.verify_txs(block)


    # TODO: change blockchain consensus: POW to POA
    def mine(self):
        while self.hash[:constants.DIFFICULTY] != '0' * constants.DIFFICULTY:
            self.nonce = self.nonce + 1
            self.hash = self.calc_hash()
        
        return self.nonce
