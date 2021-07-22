from typing import Any, List, Dict, Optional

from fastapi import Depends, APIRouter, HTTPException

from pydantic import BaseModel

from app import crud, schemas

from time import strftime,gmtime

from ..file_manager import FileManager, fileManager

router = APIRouter()

def getDb():
    return fileManager

#use for serialization the device object without 'deleted' field
class Device(BaseModel):
    id: str
    crane_id: str
    s_n: str
    model: str
    description: str
    created: str
    updated: str



@router.get("/health", response_model=None)
def get_health() -> Any:
    pass

@router.post("/device/deleted/{id}/restore", response_model=Any)
async def restore_device(
    id:str
) -> Any:
    await crud.devices.restore_device(id)
     

@router.get("/devices/deleted", response_model=List[Device])
def get_deleted_devices(
    db:Any = Depends(getDb)
) -> List:
    return crud.devices.get_all_devices(db, deleted=True)

@router.get("/devices", response_model=List)
def get_devices(
    db:Any = Depends(getDb)
) -> List:
    return crud.devices.get_all_devices(db, deleted=False)

@router.post("/devices", response_model=Any)
async def post_devices(
    id: str,
    crane_id: str,
    s_n: str,
    model: str,
    description: str
) -> Any:
    return await crud.devices.handle_post(id, crane_id, s_n, model, description)

@router.get("/devices/{id}", response_model=Dict)
def get_device(
    id: str
) -> Dict:
    return crud.devices.get_not_deleted_device(id)

@router.put("/devices/{id}", response_model=Any)
async def put_device(
    id: str,
    crane_id: Optional[str] = None,
    s_n: Optional[str] = None,
    model: Optional[str] = None,
    description: Optional[str] = None
) -> Any:
    return await crud.devices.handle_put(id, crane_id, s_n, model, description)


@router.delete("/devices/{id}", response_model=Any)
async def delete_device(
    id: str
) -> Any:
    return await crud.devices.handle_delete(id)

