# External
from typing import Dict
import copy
import sys

sys.path.append('..')

# Internal
#import core.configs.constants as constants
from consensus.challenger import Challenger
from consensus.challenge import Challenge
from consensus.mission import Mission
from consensus.team import Team

# TODO: think about validation

class ChallengerService:
    def __init__(self) -> None:        
        self.teams: Dict[str, Challenger] = {}
        self.mission: Mission = self.get_mission()

    def __str__(self) -> str:
        return f'\tChallengerService:\n\
            Teams: {len(self.teams)}\n\
            {self.mission}\n'

    # TODO: load real data (generate or get broadcasted)
    def get_mission(self) -> Mission:
        challenges = [
            Challenge(1, 'Buy coffee'),
            Challenge(2, 'Finish university test'),
            Challenge(3, 'Wash the dishes'),
            Challenge(4, 'Wash the dishes'),
            Challenge(5, 'Wash the dishes')
        ]

        mission = Mission(1, challenges)
        return mission

    def get_teams(self):
        return copy.deepcopy(self.teams)

    def get_team(self, team_hash: str) -> Team:
        return self.teams[team_hash]

    def add_team(self, chr: Challenger) -> Team:
        team = Team(chr.addr, {})
        team.add_chr(chr)
        self.teams[chr.addr] = team
        
        return self.teams[chr.addr]

    # Connect to a team
    def cnt_team(self, team_hash, chr: Challenger):
        # TODO: validate team, validate challenger

        self.teams[team_hash].add_chr(chr)

        return self.teams[team_hash]

    # Disconnect from a team
    def discnt_team(self, team_hash, chr_hash):
        # TODO: validate team, validate challenger
        teams = self.get_teams()

        teams[team_hash].del_chr(chr_hash)

        if teams[team_hash].chr_len() == 0:
            del teams[team_hash]

        self.teams = teams

        return teams.get(team_hash, {})

if __name__ == '__main__':
    service = ChallengerService()
    print(service)