import json
from json.decoder import JSONDecodeError

import time
from threading import Lock

from app.core.config import settings
from fastapi import HTTPException



lock = Lock()

def validate_crane(crane_id):
    cranes = fileManager.read_file(settings.CRANES_JSON)
    if crane_id not in cranes:
        raise HTTPException(400, detail="this crane doesnt exist")
    return True

class FileManager(object):
    def read_file(self, path = settings.DEVICES_JSON):
        try:
            with open(path) as f:
                data = json.load(f)
        except JSONDecodeError:
            data = []
        return data

        try:
            f = open(path,"r")
            data = json.load(f.read())
            print(data)
        except:
            raise HTTPException(504,'Error reading from db')
        finally:
            f.close()
        return data

    async def write_to_file(self, data, update = False):
        file_data = self.read_file()
        validate_crane(data.get('crane_id'))
        if(update):
            for i in range(len(file_data)):
                if(file_data[i].get('id') == data.get('id')):
                    file_data[i] = data
                    break
        else:
            file_data.append(data)

        lock.acquire()
        try:
            with open(settings.DEVICES_JSON, "w") as outfile:
                json.dump(file_data, outfile)
        finally:
            lock.release()


fileManager = FileManager()