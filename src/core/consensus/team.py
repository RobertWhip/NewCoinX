# External
from typing import Dict, List

# Internal
from consensus.challenger import Challenger

# TODO: should this class include hash?

class Team:
    def __init__(self, id, challengers: Dict[str, Challenger]) -> None:
        self.id = id
        self.challengers = challengers
        self.mission_access = False
        self.upd_mission_access()

    def __str__(self) -> str:
        return f'\tTeam:\n\
            ID: {self.id}\n\
            Has mission access: {self.mission_access}\n\
            Challengers: {len(self.challengers)}\n'

    def upd_mission_access(self):
        self.mission_access = self.chr_len() > 1
        return self.mission_access # TODO: remove harcoding; add config

    def add_chr(self, chr: Challenger) -> bool:
        self.challengers[chr.addr] = chr
        self.upd_mission_access()
        return True

    def del_chr(self, chr_hash: str) -> bool:
        del self.challengers[chr_hash]
        self.upd_mission_access()
        return True

    def chr_len(self) -> int:
        return len(self.challengers.keys())

if __name__ == '__main__':
    challengers = [
        Challenger('1'),
        Challenger('2'),
        Challenger('3')
    ]

    team = Team(1, challengers)
    print('Team:\n', team)

    print('Challenges:')
    for x in team.challengers:
        print(x)