# TODO: should this class include hash?

class Challenger:
    def __init__(self, addr: str) -> None:
        self.addr = addr

    def __str__(self) -> str:
        return f'\tChallenger:\n\
            Address: {self.addr}\n'