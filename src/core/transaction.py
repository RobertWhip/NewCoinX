# External
from typing import Union
import hashlib












# Internal
import configs.constants as constants
import utils.timestamp as timestamp
import configs.errors as errors
import utils.wallet as wallet
from error import Error

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

    @staticmethod
    def read(tx_dict: dict):
        tx = Tx(tx_dict['from_addr'], tx_dict['to_addr'], tx_dict['amount'])
        tx.timestamp = tx_dict['timestamp']
        tx.hash = tx_dict['hash']
        tx.signature = tx_dict['signature']

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
        if tx.from_addr == constants.MINER_BUDGET_ADDR and tx.amount != constants.REWARD:
            return False, Error(errors.ERROR_INVALID_MINING_REWARD)
        
        if tx.from_addr == None or tx.from_addr == constants.MINER_BUDGET_ADDR:
            return True, None
        
        if tx.from_addr == tx.to_addr:
            return False, Error(errors.ERROR_CANNOT_TRANFER_TO_OWN_ACCOUNT)

        if tx.amount <= 0:
            return False, Error(errors.ERROR_INVALID_AMOUNT)

        if balance is not None and balance < tx.amount:
            return False, Error(errors.ERROR_INSUFFICIENT_FUNDS_ON_THE_BALANCE)

        if tx.signature == None:
            return False, Error(errors.ERROR_INVALID_SIGNATURE)

        public_key = wallet.to_ecdsa_public(tx.from_addr)
        
        return wallet.verify_signature(
            tx.hash, 
            tx.signature, 
            public_key
        ), None

if __name__ == '__main__':
    balance_a = 5
    public_a = '2d52efa3d5a106a2e25c0ec4ae8e221f2e273cc5a208684e42a78cd46e7af4503086ab7a4542fdc96b8746612f0e3a3249f7e4703173b7b81dbc278dd449394a'
    secret_a = '6e5ccaac1aa98a87b43af3744f4ad7766aa37e815963bf8b0ace82cc888b4f18'
    public_b = 'aa08eb959f1a448aa5c61fa8d27d92dfa56f0a052560c3b1277660d2ed4ba8387ccc612e5d63f77e1881f329c3135f88b32a5cf56be65ec24906825122deef8d'

    tx = Tx(public_a, public_b, 0.05) # Створення транзакції
    tx.sign(secret_a) # Ставлення цифрового підпису на транзакцію

    print(tx)
    print('\tVerified:', Tx.is_valid(tx, balance_a))