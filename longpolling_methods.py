import hashlib
import time

LONG_POLLING_TIMING_SECONDS = 2

def longPolling(last_state_hash, getDataCallback, **args):
    output = getDataCallback(**args)
    hash = getHashFromState(output)
    while last_state_hash == hash:
        time.sleep(LONG_POLLING_TIMING_SECONDS)
        output = getDataCallback(**args)
        hash = getHashFromState(output)
    return {"state": output, "hash": getHashFromState(output)}

def getHashFromState(obj):
    if obj is not str:
        obj = str(obj)
    hash_object = hashlib.md5(obj.encode())
    return hash_object.hexdigest()