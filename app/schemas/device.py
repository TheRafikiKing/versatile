import datetime
from typing import Optional



from pydantic import BaseModel



#use for serialization the device object without for example 'deleted' field
class Device(BaseModel):
    id: str
    crane_id: str
    s_n: str
    model: str
    description: str
    created: str
    updated: str

