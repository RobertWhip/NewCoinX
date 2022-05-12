# External
from typing import Union
import plyvel
import sys

from yaml import serialize
sys.path.append('..')

# Internal
import utils.converter as conv
import configs.db as db_configs

# Abstract LevelDB model
class DBModel:
    def __init__(self, prefix) -> None:
        self.super_db = plyvel.DB(
            db_configs.DB_PATH,
            create_if_missing=True
        )
        
        self.db = self.super_db.prefixed_db(prefix.encode())

    # Save list with write_batch using LevelDB transaction
    #
    # Function arguments:
    # - list - list of dicts/objects.
    # - get_key - lambda function which is called on each elements 
    #   of 'list' list (Example: keys = [get_key(el) for el in list]).
    #
    # returns True
    def save(self, list, get_key) -> bool:
        with self.db.write_batch(transaction=True) as wb:
            for el in list:
                self.put(get_key(el), el, wb)

        return True

    # key/value serializator
    def serialize(self, text) -> bytes:
        return conv.data_2_bytes(text)

    # key/value deserializator
    def deserialize(self, bytes) -> Union[str, dict]:
        return conv.bytes_2_data(bytes)

    # Iterator generator
    def open_iter(
        self, 
        start=None, 
        stop=None, 
        snapshot=False,
        include_value=True,
        include_key=True,
        reverse=False
    ):
        db = self.db.snapshot() if snapshot else self.db

        return db.iterator(
            start=(self.serialize(start) if start else None), 
            stop=(self.serialize(stop) if stop else None),
            include_value=include_value,
            include_key=include_key,
            reverse=reverse,
        )

    # Returns next iteration
    def next(self, it):
        iteration = next(it)

        # If iterator excludes keys or values
        if type(iteration) == bytes:
            return self.deserialize(iteration)

        # Key and value
        elif type(iteration) == tuple:
            return (
                self.deserialize(iteration[0]),
                self.deserialize(iteration[1])
            )
        
        # TODO: Is it a good idea? Should we throw an error?
        else:
            return iteration

    # Close given iterator
    def close_iter(self, iterator):
        return iterator.close()

    # Get value by key
    def get(self, key):
        return self.db.get(self.serialize(key))
        
    def superdb_get(self, key):
        return self.super_db.get(self.serialize(key))
    
    # Get last element (sort by keys -> reverse it -> get first)
    def get_last_val(self):
        # open iterator in reverse order
        it = self.open_iter(reverse=True, include_key=False)

        # get first element (which is the last)
        val = self.next(it)

        # close iterator
        self.close_iter(it)

        return val # deserialized Block

    # Get last key (sort by keys -> reverse it -> get first)
    def get_last_key(self):
        # open iterator in reverse order
        it = self.open_iter(reverse=True, include_value=False)

        # get first element (which is the last)
        key = self.next(it)

        # close iterator
        self.close_iter(it)

        return key # Deserialized height


    def put(self, key, val, db=None):
        _db = db if db else self.db

        return _db.put(
            self.serialize(key),
            self.serialize(val)
        )
        
    def superdb_put(self, key, val):
        return self.super_db.put(
            self.serialize(key),
            self.serialize(val)
        )

if __name__ == '__main__':
    db = DBModel('test_')