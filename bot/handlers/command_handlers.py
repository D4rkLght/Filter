import asyncio
from datetime import datetime
from typing import Literal

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CommandHandler

from bot.constants.messages import (HELP_MESSAGE, RULES_MESSAGE, START_MESSAGE,
                                    WELCOME_1_MESSAGE, WELCOME_MESSAGE)
from bot.constants.states import States
from bot.core.settings import TIME_IN_SECONDS, settings
from bot.keyboards.command_keyboards import payment_keyboard_markup
from bot.keyboards.conversation_keyboards import remove_keyboard_markup
from bot.logging.logging import debug_logger
from bot.utils.message_senders import send_message


@debug_logger
async def start(update: Update, context: CallbackContext) -> Literal[States.GO]:
    """Функция-обработчик команды start."""
    query = update.callback_query
    if query:
        user_id = query.from_user.id
    else:
        user_id = update.message.from_user.id
    #     if user_id == settings.app_settings.telegram_user_id:
    #         await update.message.reply_text(
    #             text='Hello, admin!',
    #             write_timeout=5,
    #         )
    #         return None
    if not [job for job in context.job_queue.jobs() if job.user_id == user_id]:
        context.job_queue.run_once(  # type: ignore[attr-defined]
                callback=send_message,
                when=TIME_IN_SECONDS,
                data={"start_time": datetime.now(), "user_id": user_id},
                user_id=user_id,
            )
    await context.bot.send_message(
        chat_id=user_id,
        text=WELCOME_MESSAGE,
        reply_markup=remove_keyboard_markup,
        parse_mode=ParseMode.HTML
    )
    await asyncio.sleep(3)
    await context.bot.send_message(
        chat_id=user_id,
        text=WELCOME_1_MESSAGE,
        parse_mode=ParseMode.HTML
    )
    await asyncio.sleep(4)
    await context.bot.send_message(
        chat_id=user_id,
        text=RULES_MESSAGE,
        parse_mode=ParseMode.HTML
    )
    await asyncio.sleep(7)
    await context.bot.send_video_note(
        chat_id=user_id,
        video_note=open('bot/media/round1', 'rb'),
    )
    await asyncio.sleep(8)
    await context.bot.send_video_note(
        chat_id=user_id,
        video_note=open('bot/media/round2', 'rb'),
    )
    await asyncio.sleep(10)
    if not query:
        await update.message.reply_text(
            text=START_MESSAGE,
            reply_markup=payment_keyboard_markup,
            parse_mode=ParseMode.HTML
        )
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text=START_MESSAGE,
            reply_markup=payment_keyboard_markup,
            parse_mode=ParseMode.HTML
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
