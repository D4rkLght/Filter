from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.buttons import (
    START_BUTTON,
)

start_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text=START_BUTTON, callback_data="start"),
        ]
    ]
)
