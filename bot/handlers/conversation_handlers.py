from typing import Literal, Optional

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

from bot.constants.states import States
from bot.logging.logging import debug_logger

from bot.constants.messages import PAYMENT_MESSAGE, PAY_CARD_MESSAGE, END_MESSAGE, PAY_CRYPTO_MESSAGE, SCREENSHOT_MESSAGE, NEW_ORDER_MESSAGE, CRYPTO
from bot.keyboards.conversation_keyboards import choose_pay_keyboard_markup, back_keyboard_markup, remove_keyboard_markup

from bot.core.settings import settings

@debug_logger
async def pay(update: Update, context: CallbackContext) -> Optional[States]:
    """Обработчик кнопки "pay"."""
    if update.message:
        await update.message.reply_text(
            text=PAYMENT_MESSAGE,
            reply_markup=choose_pay_keyboard_markup,
            write_timeout=5,
        )
    return States.CHOOSE

@debug_logger
async def payment(update: Update, context: CallbackContext) -> Optional[States]:
    """Обработчик кнопки "payment"."""
    pay_text = [PAY_CRYPTO_MESSAGE, PAY_CARD_MESSAGE][CRYPTO != update.message.text.split(' ')[0]]
    if update.message:
        await update.message.reply_text(
            text=pay_text,
            reply_markup=back_keyboard_markup,
            write_timeout=5,
            disable_web_page_preview=True
        )
        await context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=SCREENSHOT_MESSAGE,
            parse_mode=ParseMode.HTML,
        )
    return States.SCREEN

@debug_logger
async def end(update: Update, context: CallbackContext) -> Optional[States]:
    """Обработчик кнопки "end"."""
    query = update.message
    user = query.from_user
    if query:
        await update.message.reply_text(
            text=END_MESSAGE,
            reply_markup=remove_keyboard_markup
        )
        await context.bot.send_message(
            chat_id=settings.app_settings.telegram_user_id,
            text=NEW_ORDER_MESSAGE.format(
                user.id,
                user.first_name or 'no name',
                user.username,
                f'https://t.me/{user.username}',
            ),
            parse_mode=ParseMode.HTML,
        )
        # send message to spetial telegram user about info new client.
    return None
