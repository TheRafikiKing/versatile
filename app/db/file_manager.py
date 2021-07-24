import json
from json.decoder import JSONDecodeError
from threading import Lock



from fastapi import HTTPException



from app.core.config import settings



lock = Lock()




async def validate_crane(crane_id):
    cranes = await fileManager.read_file(settings.CRANES_JSON)
    if crane_id not in cranes:
        raise HTTPException(400, detail="this crane doesnt exist")
    return True

class FileManager(object):
    async def read_file(self, path = settings.DEVICES_JSON):
        try:

            with open(path) as f:
                data = json.load(f)

        except JSONDecodeError:
            data = []
        except OSError as e:
            if e.errno == errno.ENOENT:
                HTTPException(504, 'File not found')
            elif e.errno == errno.EACCES:
                HTTPException(504, 'Permission denied')
            else:
                HTTPException(504, f'Unexpected error: {e.errno}')

        return data

    async def write_to_file(self, data, update = False):
        file_data = await self.read_file()
        await validate_crane(data.get('crane_id'))
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

        except OSError as e:
            if e.errno == errno.ENOENT:
                HTTPException(504, 'File not found')
            elif e.errno == errno.EACCES:
                HTTPException(504, 'Permission denied')
            else:
                HTTPException(504, f'Unexpected error: {e.errno}')

        finally:
            lock.release()


fileManager = FileManager()