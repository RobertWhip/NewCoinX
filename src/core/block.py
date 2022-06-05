# External
from typing import Tuple
from typing import List
import hashlib
import json
import sys

sys.path.append('..')

# Internal
import configs.constants as constants
import utils.timestamp as timestamp
import configs.errors as errors
from transaction import Tx
from error import Error

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
        if block.txs is None or len(block.txs) <= 0:
            return False, Error(errors.ERROR_TRANSACTIONS_NOT_FOUND)

        for tx in block.txs:
            is_tx_valid, tx_error = Tx.is_valid(tx, None)

            if not is_tx_valid:
                return False, tx_error

        return True, None

    @staticmethod
    def verify_hash(block):
        if block.hash != block.calc_hash():
            return False, Error(errors.ERROR_INVALID_BLOCK_HASH)

        if block.hash[:constants.DIFFICULTY] != '0' * constants.DIFFICULTY:
            return False, Error(errors.ERROR_INVALID_HASH_DIFFICULTY)

        return True, None

    @staticmethod
    def is_valid(block) -> bool:
        txs_verified, txs_error = Block.verify_txs(block)
        hash_verified, hash_error = Block.verify_hash(block)

        if not txs_verified:
            return False, txs_error

        if not hash_verified:
            return False, hash_error

        return True, None

    def mine(self):
        while self.hash[:constants.DIFFICULTY] != '0' * constants.DIFFICULTY:
            self.nonce = self.nonce + 1
            self.hash = self.calc_hash()
        
        return self.nonce

    @staticmethod
    def read(bl_dict: dict):
        txs = [Tx.read(tx) for tx in bl_dict['txs']]

        block = Block(txs, bl_dict['prev_hash'], bl_dict['height'])
        
        block.timestamp = bl_dict['timestamp']
        block.nonce = bl_dict['nonce']
        block.hash = bl_dict['hash']

        return block

if __name__ == '__main__':
    from timeit import default_timer as timer

    balance_a = 5
    public_a = '2d52efa3d5a106a2e25c0ec4ae8e221f2e273cc5a208684e42a78cd46e7af4503086ab7a4542fdc96b8746612f0e3a3249f7e4703173b7b81dbc278dd449394a'
    secret_a = '6e5ccaac1aa98a87b43af3744f4ad7766aa37e815963bf8b0ace82cc888b4f18'
    public_b = 'aa08eb959f1a448aa5c61fa8d27d92dfa56f0a052560c3b1277660d2ed4ba8387ccc612e5d63f77e1881f329c3135f88b32a5cf56be65ec24906825122deef8d'

    tx0 = Tx(public_a, public_b, 0.05) # Створення транзакції
    tx1 = Tx(public_a, public_b, 0.3) # Створення транзакції
    tx0.sign(secret_a) # Ставлення цифрового підпису на транзакцію
    tx1.sign(secret_a) # Ставлення цифрового підпису на транзакцію
    prev_hash = 'Hash of previous block'
    height = 2 # Висота попереднього блока + 1

    new_block = Block([tx0, tx1], prev_hash, height) # Створення блоку


    start = timer()
    new_block.mine() # Майнінг блоку...
    end = timer()

    print(new_block) # На цьому кроці хеш знайдений
    print('Mining took', end - start, 'seconds')
    print('Verified:', Block.is_valid(new_block))