from typing import Literal, Optional
# from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext

from bot.constants.states import States
from bot.logging.logging import debug_logger

from bot.core.settings import settings


@debug_logger
async def pay(update: Update, context: CallbackContext) -> Optional[States]:
    """Обработчик кнопки "shop"."""
    query = update.callback_query
    # while doesn't server
    # await query.answer("Hello", show_alert=True, url=settings.app_settings.url.format(context.user_data.get("user_id")))
    await query.answer("Hello", show_alert=True, url=settings.app_settings.url_test.format(context.user_data.get("user_id")))
    return States.TEST
