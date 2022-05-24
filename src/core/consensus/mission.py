# External
from typing import List

# Internal
from consensus.challenge import Challenge

# TODO: should this class include hash?

class Mission:
    def __init__(self, id, challenges: List[Challenge]) -> None:
        self.id = id
        self.challenges = challenges

    def __str__(self) -> str:
        return f'\tMission:\n\
            ID: {self.id}\n\
            Challenges: {len(self.challenges)}\n'

if __name__ == '__main__':
    challenges = [
        Challenge(1, 'Buy coffee'),
        Challenge(2, 'Finish university test'),
        Challenge(3, 'Wash the dishes')
    ]

    mission = Mission(1, challenges)
    print('Mission:\n', mission)

    print('Challenges:')
    for x in mission.challenges:
        print(x)