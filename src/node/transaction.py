import hashlib
import timestamp


class Tx:
    def __init__(self, from_addr, to_addr, amount) -> None:
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount
        self.timestamp = timestamp.now()
        self.hash = self.calc_hash()

    def __str__(self) -> str:
        return f' Transaction:\n\
            Hash: {self.hash}\n\
            From: {self.from_addr}\n\
            To: {self.to_addr}\n\
            Amount: {self.amount}\n\
            Timestamp: {self.timestamp}'
    
    def calc_hash(self) -> str:
        return hashlib.sha256(
            (
                self.from_addr + 
                self.to_addr + 
                str(self.timestamp) +
                str(self.amount)
            ).encode('utf-8')
        ).hexdigest()


if __name__ == '__main__':
    print(Tx('1', '2', 3))