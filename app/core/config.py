import os
import secrets
from typing import Any, Dict, List, Optional, Union



from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, validator




class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = 'localhost'

    HTTP_PORT =  os.getenv('HTTP_PORT')
    DEVICES_JSON = os.getenv('DEVICES_JSON')
    CRANES_JSON =  os.getenv('CRANES_JSON')

    SERVER_HOST: AnyHttpUrl = os.getenv('SERVER_HOST','http://localhost:8000')
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        'http://localhost:' + str(HTTP_PORT) ,'http://localhost:8080','http://localhost:4200',SERVER_HOST
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = 'versatile'


    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    class Config:
        case_sensitive = True


settings = Settings()