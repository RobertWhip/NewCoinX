# External
from typing import Dict, List
import pickle
import json

def to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)

def data_2_bytes(obj):
    return pickle.dumps(obj)

def bytes_2_data(bytes):
    return pickle.loads(bytes)

# TODO: refactor next 3 functions
def obj_2_dict(obj, obj_types) -> dict:
    if type(obj) == dict:
        return obj

    obj = vars(obj)

    for key in obj.keys():
        if type(obj[key]) == list:
            obj[key] = list_obj_2_list_dict(obj[key], obj_types)
        elif type(obj[key]) == dict:
            obj[key] = dict_w_obj_2_dict(obj[key], obj_types)
        elif type(obj[key]) == bytes:
            obj[key] = str(obj[key])
        elif type(obj[key]) in obj_types:
            obj[key] = obj_2_dict(obj[key], obj_types)
            
    return obj

def dict_w_obj_2_dict(dict_with_obj, obj_types) -> Dict:
    for key in dict_with_obj.keys():
        if type(dict_with_obj[key]) in obj_types:
            dict_with_obj[key] = obj_2_dict(dict_with_obj[key], obj_types)

    return dict_with_obj

def list_obj_2_list_dict(list, obj_types) -> List[dict]:
    # TODO: do we need this condition here?
    if len(list) == 0:
        return list

    for i in range(len(list)):
        if type(list[i]) == list:
            list[i] = list_obj_2_list_dict(list[i], obj_types)
        elif type(list[i]) in obj_types:
            list[i] = obj_2_dict(list[i], obj_types)

    return list
