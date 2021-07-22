from typing import Optional
import datetime

from pydantic import BaseModel


#use for serialization the device object without 'deleted' field
class Device(BaseModel):
    id: str
    crane_id: str
    s_n: str
    model: str
    description: str
    created: str
    updated: str

