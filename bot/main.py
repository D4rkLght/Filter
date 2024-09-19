from http import HTTPStatus
from loguru import logger
from typing import Any
from httpx import AsyncClient, Request, Response

from fastapi import Depends, FastAPI, status, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse
from uvicorn import run

from bot.core.settings import settings
from bot.logging.logging import setup_logger
from bot.middlewares import middleware
from bot.bot import Bot


IS_DEBUG: bool = settings.app_settings.is_debug or False
LOG_LEVEL: str = settings.app_settings.log_level or "INFO"

log_config: dict[str, Any] = setup_logger(
    logger_level=LOG_LEVEL,
)


bot = Bot()


async def startup() -> None:
    await bot.start()



async def shutdown() -> None:
    bot.stop()


router = APIRouter()


def get_application() -> FastAPI:
    app: FastAPI = FastAPI(
        title="Filter",
        default_response_class=ORJSONResponse,
        middleware=middleware,
        docs_url=None,
        openapi_url=None,
        debug=IS_DEBUG,
    )
    app.include_router(router)

    app.add_event_handler(
        event_type="startup",
        func=startup,
    )

    app.add_event_handler(
        event_type="shutdown",
        func=shutdown,
    )


    return app


app: FastAPI = get_application()

if __name__ == "__main__":
    run(
        app=app,
        host=settings.app_settings.wsgi_host,
        port=int(settings.app_settings.wsgi_port),
        use_colors=True,
        reload=IS_DEBUG,
    )
