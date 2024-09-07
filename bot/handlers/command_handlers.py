from typing import Literal, Optional

from uuid import uuid4
from telegram import Update
from telegram.constants import ParseMode, ChatAction
from telegram.ext import CallbackContext, CommandHandler


from bot.constants.states import States
from bot.keyboards.command_keyboards import (
    start_keyboard_markup,
)

from bot.logging.logging import debug_logger
from bot.core.settings import settings

@debug_logger
async def start(update: Update, context: CallbackContext) -> Literal[States.START]:
    """Функция-обработчик команды start."""
    context.user_data["user_id"] = update.message.from_user.id
    if update.message:
        await update.message.reply_text(
            text='STORY_MESSAGE',
            reply_markup=start_keyboard_markup,
            parse_mode=ParseMode.HTML,
            write_timeout=5,
        )
    # await context.bot.send_message(
    #     chat_id=update.message.from_user.id,
    #     text=form_recruiter.format(
    #         recruiter.name,
    #         "It-рекрутер",
    #         recruiter.telegram_username,
    #         guide_url,
    #     ),
    #     parse_mode=ParseMode.HTML,
    # )
    # return States.START


start_handler = CommandHandler("start", start)

















