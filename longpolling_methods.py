import hashlib
import time

def longPolling(last_state_hash, getDataCallback, counter=30,  **args):
    output = getDataCallback(**args)
    hash = getHashFromState(output) 
    while last_state_hash == hash or counter > 0:
        counter -= 1
        time.sleep(1)
        output = getDataCallback(**args)
        hash = getHashFromState(output)
    return {"state": output, "hash": getHashFromState(output)}

def getHashFromState(obj):
    if obj is not str:
        obj = str(obj)
    hash_object = hashlib.md5(obj.encode())
    return hash_object.hexdigest()