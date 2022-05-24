# TODO: should this class include hash?

class Challenge:
    def __init__(self, id, desc: str) -> None:
        self.id = id
        self.desc = desc

    def __str__(self) -> str:
        return f'\tChallenge:\n\
            ID: {self.id}\n\
            Description: {self.desc}\n'