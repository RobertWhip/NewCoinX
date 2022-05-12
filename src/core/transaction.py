# External
from typing import Union
import hashlib

# Internal
import configs.constants as constants
import utils.timestamp as timestamp
import configs.errors as errors
import utils.wallet as wallet
from error import Error

'''
    TODO:
        1. implement UTXO
        2. improve tx validation
        3. think what fields should we add
'''

class Tx:
    def __init__(
        self, 
        from_addr: str, 
        to_addr: str, 
        amount: int
    ) -> None:
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount
        self.timestamp = timestamp.now()
        self.hash = self.calc_hash()
        self.signature = None

    # TODO: do we need this function?
    @staticmethod
    def from_dict(dict: dict):
        tx = Tx(
            dict.from_addr,
            dict.to_addr,
            dict.amount
        )

        tx.timestamp = dict.timestamp
        tx.hash = dict.hash
        tx.signature = dict.signature

        return tx

    def __str__(self) -> str:
        return f' \tTransaction:\n\
            Hash: {self.hash}\n\
            From: {self.from_addr}\n\
            To: {self.to_addr}\n\
            Amount: {self.amount}\n\
            Timestamp: {self.timestamp}\n'
    

    def calc_hash(self) -> str:
        return hashlib.sha256(
            (
                self.from_addr + 
                self.to_addr + 
                str(self.timestamp) +
                str(self.amount)
            ).encode('utf-8')
        ).hexdigest()


    def sign(self, private_key) -> Union[bool, Error]:
        private_key = wallet.to_ecdsa_private(private_key)

        if wallet.to_hex(wallet.ecdsa_private_to_public(private_key)) != self.from_addr:
            return Error(errors.ERROR_INVALID_PRIVATE_KEY)

        tx_hash = self.calc_hash()
        self.signature = wallet.create_signature(
            tx_hash,
            private_key
        )

        return True

    @staticmethod
    def is_valid(tx, balance) -> tuple([bool, Error]):
        # TODO: do not reject the TX, but set the correct reward. 
        # Also think about mining reward TX validation 
        if tx.from_addr == constants.MINER_BUDGET_ADDR and tx.amount != constants.REWARD:
            return False, Error(errors.ERROR_INVALID_MINING_REWARD)
        
        if tx.from_addr == None or tx.from_addr == constants.MINER_BUDGET_ADDR:
            return True, None
        
        if tx.from_addr == tx.to_addr:
            return False, Error(errors.ERROR_CANNOT_TRANFER_TO_OWN_ACCOUNT)

        if tx.amount < 0:
            return False, Error(errors.ERROR_INVALID_AMOUNT)

        if balance is not None and balance < tx.amount:
            return False, Error(errors.ERROR_INSUFFICIENT_FUNDS_ON_THE_BALANCE)

        if tx.signature == None:
            return False, Error(errors.ERROR_INVALID_SIGNATURE)

        # TODO: catch error
        public_key = wallet.to_ecdsa_public(tx.from_addr)
        
        return wallet.verify_signature(
            tx.hash, 
            tx.signature, 
            public_key
        ), None



if __name__ == '__main__':
    print(Tx('1', '2', 3))