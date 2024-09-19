from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware import Middleware


middleware = [
    Middleware(
        CORSMiddleware,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origins=["*"],
        allow_credentials=True,
    ),
    Middleware(
        GZipMiddleware,
        minimum_size=50,
    ),
]
