from typing import Literal

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CommandHandler


from bot.constants.states import States
from bot.keyboards.command_keyboards import (
    start_keyboard_markup,
    payment_keyboard_markup
)

from bot.logging.logging import debug_logger
from bot.core.settings import settings
from bot.constants.messages import START_MESSAGE, WELCOME_MESSAGE, WELCOME_1_MESSAGE, RULES_MESSAGE

@debug_logger
async def start(update: Update, context: CallbackContext) -> Literal[States.GO]:
    """Функция-обработчик команды start."""
    if update.message:
        await context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=WELCOME_MESSAGE,
            parse_mode=ParseMode.HTML,
        )
        await context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=WELCOME_1_MESSAGE,
            parse_mode=ParseMode.HTML,
        )
        await context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=RULES_MESSAGE,
            parse_mode=ParseMode.HTML,
        )
        await context.bot.send_video_note(
            chat_id=update.message.from_user.id,
            video_note=open('bot/handlers/round', 'rb')
        )
        await update.message.reply_text(
            text=START_MESSAGE,
            reply_markup=payment_keyboard_markup,
            write_timeout=5,
        )
    return States.GO


start_handler = CommandHandler("start", start)










