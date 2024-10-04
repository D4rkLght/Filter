import asyncio
from typing import Optional

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

from bot.constants.messages import (BOTH, CRYPTO, END_MESSAGE, HELP_MESSAGE,
                                    NEW_ORDER_MESSAGE, PAY_CARD_MESSAGE,
                                    PAY_CRYPTO_MESSAGE, PAYMENT_MESSAGE,
                                    POSSIBLE_OPTINONS, SCREENSHOT_MESSAGE,
                                    SUPPORT_MESSAGE)
from bot.constants.states import States
from bot.core.settings import settings
from bot.keyboards.command_keyboards import payment_keyboard_markup
from bot.keyboards.conversation_keyboards import (back_keyboard_markup,
                                                  choose_pay_keyboard_markup,
                                                  remove_keyboard_markup)
from bot.logging.logging import debug_logger


@debug_logger
async def pay(update: Update, context: CallbackContext) -> Optional[States]:
    """Обработчик кнопки "pay"."""
    if update.message:
        if update.message.text in POSSIBLE_OPTINONS:
            await update.message.reply_text(
                text=PAYMENT_MESSAGE,
                reply_markup=choose_pay_keyboard_markup,
                write_timeout=5,
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_text(
                text=SUPPORT_MESSAGE,
                reply_markup=payment_keyboard_markup,
                write_timeout=5,
                parse_mode=ParseMode.HTML
            )
            return States.GO
    return States.CHOOSE


@debug_logger
async def check_text(update: Update, context: CallbackContext) -> Optional[States]:
    """Обработчик кнопки "check_text"."""
    if update.message:
        if update.message.text == "Go back":
            await update.message.reply_text(
                text=PAYMENT_MESSAGE,
                reply_markup=choose_pay_keyboard_markup,
                write_timeout=5,
                parse_mode=ParseMode.HTML
            )
        elif update.message.text == "Need help!":
            await update.message.reply_text(
                text=HELP_MESSAGE,
                write_timeout=5,
                parse_mode=ParseMode.HTML
            )
    return States.CHOOSE


@debug_logger
async def payment(update: Update, context: CallbackContext) -> Optional[States]:
    """Обработчик кнопки "payment"."""
    text = update.message.text
    if text not in BOTH:
        text = [SUPPORT_MESSAGE, PAYMENT_MESSAGE][text == "Go back"]
        await update.message.reply_text(
                text=text,
                reply_markup=choose_pay_keyboard_markup,
                write_timeout=5,
                parse_mode=ParseMode.HTML
            )
        return States.CHOOSE
    pay_text = [PAY_CRYPTO_MESSAGE, PAY_CARD_MESSAGE][CRYPTO != text]
    if update.message:
        await update.message.reply_text(
            text=pay_text,
            reply_markup=back_keyboard_markup,
            write_timeout=5,
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
        )
        await asyncio.sleep(3)
        await context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=SCREENSHOT_MESSAGE,
            parse_mode=ParseMode.HTML
        )
    return States.SCREEN


@debug_logger
async def end(update: Update, context: CallbackContext) -> Optional[States]:
    """Обработчик кнопки "end"."""
    query = update.message
    user = query.from_user
    if query:
        [job.schedule_removal() for job in context.job_queue.jobs() if job.user_id == user.id]
        await update.message.reply_text(
            text=END_MESSAGE,
            reply_markup=remove_keyboard_markup,
            parse_mode=ParseMode.HTML
        )
        await context.bot.send_photo(
            chat_id=settings.app_settings.telegram_user_id,
            photo=query.photo[-1].file_id,
            caption=NEW_ORDER_MESSAGE.format(
                user.id,
                user.first_name or 'no name',
                user.username,
                f'https://t.me/{user.username}',
            ),
            show_caption_above_media=True
        )
    return None
