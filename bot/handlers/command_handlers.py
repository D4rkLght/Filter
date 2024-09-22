import asyncio
from typing import Literal

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CommandHandler

from bot.constants.messages import (HELP_MESSAGE, RULES_MESSAGE, START_MESSAGE,
                                    WELCOME_1_MESSAGE, WELCOME_MESSAGE)
from bot.constants.states import States
from bot.core.settings import settings
from bot.keyboards.command_keyboards import (payment_keyboard_markup,
                                             start_keyboard_markup)
from bot.logging.logging import debug_logger


@debug_logger
async def start(update: Update, context: CallbackContext) -> Literal[States.GO]:
    """Функция-обработчик команды start."""
    if update.message:
        if update.message.from_user.id == settings.app_settings.telegram_user_id:
            await update.message.reply_text(
                text='Hello, admin!',
                write_timeout=5,
            )
            return None
        await context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=WELCOME_MESSAGE,
        )
        await asyncio.sleep(3)
        await context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=WELCOME_1_MESSAGE,
        )
        await asyncio.sleep(4)
        await context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=RULES_MESSAGE,
        )
        await asyncio.sleep(7)
        await context.bot.send_video_note(
            chat_id=update.message.from_user.id,
            video_note=open('bot/media/round', 'rb'),
        )
        await asyncio.sleep(10)
        await update.message.reply_text(
            text=START_MESSAGE,
            reply_markup=payment_keyboard_markup,
        )
    return States.GO


@debug_logger
async def help(update: Update, context: CallbackContext) -> Literal[States.GO]:
    """Функция-обработчик команды help."""
    await update.message.reply_text(
        text=HELP_MESSAGE,
        write_timeout=5,
    )
    return None


start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help)
