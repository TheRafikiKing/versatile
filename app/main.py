import os



import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException



from app.api.api import api_router
from app.core.config import settings



app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"/openapi.json"
)

# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# @app.exception_handler(StarletteHTTPException)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)