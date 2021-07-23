from typing import Any, List, Dict, Optional

from fastapi import HTTPException
from time import strftime,gmtime


from app.schemas.device import Device
from app.db.file_manager import fileManager


#region helper funnctions
#TBD - make helper file and move helper functions
def get_timestamp():
    return strftime("%d/%m/%Y %H:%M:%S", gmtime())

def find_device(id, s_n=None):
    devices_lst = fileManager.read_file()
    # if we prepare for post
    # we scan to find existing options
    if(s_n):
        return list(
            filter(
                lambda x: x.get('id') == id or x.get('s_n') == s_n,
                devices_lst
                )
            )
    return list(
        filter(
            lambda x: x.get('id') == id ,
            devices_lst
            )
        )

def get_device(id,status_code=404):
    result = find_device(id)
    try:
        return result[0]
    except:
        raise HTTPException(status_code=404,detail="device not found")

def get_not_deleted_device(id):
    devices_lst = fileManager.read_file()
    result = list(
        filter(
            lambda x: x.get('id') == id and x.get('deleted') == 'false' ,
            devices_lst
            )
        )
    try:
        return result[0]
    except:
        raise HTTPException(status_code=404,detail="device not found")

# TBD - better naming
def get_all_devices(db, deleted=False):
    devices_list = db.read_file()
    if(deleted):
        deleted = 'true'
    else:
        deleted = 'false'
    return list(filter(lambda x: x.get('deleted') == deleted, devices_list))

#endregion helper functions

class CRUDDevice():
    async def restore_device(self, id:str):
        item = get_device(id)
        if(item['deleted'] == 'true'):
            item['deleted'] = 'false'
        return await fileManager.write_to_file(item, update=True)

    def get_all_devices(self, db, deleted: bool):
        return get_all_devices(db,deleted)

    async def handle_post(
        self,
        id: str,
        crane_id: str,
        s_n: str,
        model: str,
        description: str
        ):
        item = find_device(id, s_n)
        if(len(item) == 1):
            if(
                item[0].get('id') == id 
                and item[0].get('s_n') == s_n 
                and item[0].get('model') == model
            ):
                item[0]['crane_id'] = crane_id
                item[0]['description'] = description
                item[0]['updated'] = get_timestamp()

                await fileManager.write_to_file(item[0], update=True)
                return {"msg":"device was updated succesfully"}
            else:
                raise HTTPException(status_code=409,detail="device already exists")
        elif(len(item) == 0):
            new_device = {
                "id": id ,  
                "crane_id": crane_id, 
                "s_n": s_n,
                "model": model,
                "description": description, 
                "created": get_timestamp(),
                "updated": get_timestamp(),
                "deleted": "false"
            }
            await fileManager.write_to_file(new_device)
            return {"msg":"device was addeed succesfully"}
        else:
            raise HTTPException(status_code=404,detail="device already exists")

    def get_not_deleted_device(self, id:str):
        return get_not_deleted_device(id)
    
    async def handle_put(
        self,
        id: str,
        crane_id: Optional[str] = None,
        s_n: Optional[str] = None,
        model: Optional[str] = None,
        description: Optional[str] = None
        ):
        device = get_device(id)
        if(crane_id):
            device['crane_id'] = crane_id
        else:
            device['crane_id'] = 'no_crane'
        if(s_n):
            device['s_n'] = s_n
        if(model):
            device['model'] = model
        if(description):
            device['description'] = description
        device['updated'] = get_timestamp()
        
        await fileManager.write_to_file(device, update=True)

        return {'msg':'devices data updated'}

    async def handle_delete(self, id: str):
        item = get_device(id)
        if(item['deleted'] == 'false'):
            item['deleted'] = 'true'
            await fileManager.write_to_file(item, update=True)
        return {'msg':'device has been deleted succesfully'} 



devices = CRUDDevice()