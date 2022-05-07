import hashlib
import timestamp

class Block:
    def __init__(
        self,
        index,
        txs,
        prev_hash
    ) -> None:
        self.index = index
        self.txs = txs
        self.prev_hash = prev_hash
        self.timestamp = timestamp.now()
        self.hash = self.calc_hash()

    def __str__(self) -> str:
        return f' Block:\n\
            Hash: {self.hash}\n\
            Previous hash: {self.prev_hash}\n\
            index: {self.index}\n\
            Timestamp: {self.timestamp}\n\
            TXs: {[tx.hash for tx in self.txs]}'

    def calc_hash(self) -> str:
        return hashlib.sha256(
            (
                str(self.index) + 
                ''.join([tx.hash for tx in self.txs]) + 
                self.prev_hash + 
                str(self.timestamp)
            ).encode('utf-8')
        ).hexdigest()