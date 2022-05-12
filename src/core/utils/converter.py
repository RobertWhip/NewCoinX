# External
import pickle
import json

def to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)

def data_2_bytes(obj):
    return pickle.dumps(obj)

def bytes_2_data(bytes):
    return pickle.loads(bytes)