# Internal
from utils.converter import dict_w_obj_2_dict, obj_2_dict
from core.blockchain import BlockchainCore
from node import app, request

from consensus.challenger import Challenger
from consensus.challenge import Challenge
from consensus.mission import Mission
from consensus.team import Team

# TODO: refactor this
obj_types = [type(Team('', {})), type(Challenger(''))]

@app.route('/v1/chr/teams', methods=['GET'])
def get_teams():
    blockchain = BlockchainCore()

    return dict_w_obj_2_dict(
        blockchain.chrService().get_teams(),
        obj_types
    )
    
@app.route('/v1/chr/team', methods=['GET'])
def get_team():
    blockchain = BlockchainCore()

    hash = request.args.get('hash', default = '', type = str)
    team = blockchain.chrService().get_team(hash)

    return obj_2_dict(
        team,
        obj_types
    )

@app.route('/v1/chr/teams', methods=['POST'])
def add_team():
    blockchain = BlockchainCore()

    chr = Challenger(request.json['addr'])

    return obj_2_dict(
        blockchain.chrService().add_team(chr),
        obj_types
    )

@app.route('/v1/chr/team/connect', methods=['POST'])
def add_chr():
    blockchain = BlockchainCore()

    team_hash = request.json['team_hash']
    chr_hash = request.json['chr_hash']

    chr = Challenger(chr_hash)

    return obj_2_dict(
        blockchain.chrService().cnt_team(team_hash, chr),
        obj_types
    )

@app.route('/v1/chr/team/disconnect', methods=['DELETE'])
def del_chr():
    blockchain = BlockchainCore()

    team_hash = request.json['team_hash']
    chr_hash = request.json['chr_hash']
    
    return obj_2_dict(
        blockchain.chrService().discnt_team(team_hash, chr_hash),
        obj_types
    )

@app.route('/v1/chr/get_mission', methods=['POST'])
def get_mission():
    blockchain = BlockchainCore()
    return obj_2_dict(
        blockchain.chrService().get_mission(),
        [type(Mission('', [])), type(Challenge('', ''))]
    )
