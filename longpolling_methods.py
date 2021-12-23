import hashlib

def getHashFromState(obj):
    if obj is not str:
        obj = str(obj)
    hash_object = hashlib.md5(obj.encode())
    return hash_object.hexdigest()