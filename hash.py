import hashlib

from termcolor import cprint

from constants import COLOR_ERROR


def is_hash_supported(hash_func):
    if hash_func.lower() == 'sha1' or hash_func.lower() == 'sha-1':
        return True
    cprint('Given hash function is not supported', COLOR_ERROR)
    return False


def hashing(file_path):
    block_size = 65536
    hash_obj = hashlib.sha1()
    with open(file_path, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hash_obj.update(buf)
            buf = f.read(block_size)
    return hash_obj.hexdigest()
