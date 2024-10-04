from typing import Any

from fastapi import APIRouter, FastAPI, Request
from loguru import logger
from telegram import Update
from telegram.ext import ApplicationBuilder
from uvicorn import run

from bot.bot import Bot
from bot.core.settings import WEBHOOK_PATH, settings
from bot.logging.logging import setup_logger
from bot.middlewares import middleware

IS_DEBUG: bool = settings.app_settings.is_debug or False
LOG_LEVEL: str = settings.app_settings.log_level or "INFO"

log_config: dict[str, Any] = setup_logger(
    logger_level=LOG_LEVEL,
)


bot = Bot()
application = ApplicationBuilder().token(settings.app_settings.telegram_token).build()


async def startup() -> None:
    await bot.start(application)


async def shutdown() -> None:
    bot.stop()


router = APIRouter()


def get_application() -> FastAPI:
    app: FastAPI = FastAPI(
        title="Filter",
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


@app.post(WEBHOOK_PATH)
async def handle_webhook(request: Request):
    try:
        # Get the update from the request body
        update = Update.de_json(await request.json(), application.bot)
        # Process the update
        await application.process_update(update)

        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling update: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    run(
        app=app,
        host=settings.app_settings.wsgi_host,
        port=int(settings.app_settings.wsgi_port),
        use_colors=True,
        reload=IS_DEBUG,
    )
