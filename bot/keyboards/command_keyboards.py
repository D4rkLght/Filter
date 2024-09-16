from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from bot.constants.buttons import (
    START_BUTTON,
    PAYMENT_BUTTON
)

start_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text=START_BUTTON, callback_data="go"),
        ]
    ]
)

payment_keyboard_markup = ReplyKeyboardMarkup([
    [
        PAYMENT_BUTTON
    ]], resize_keyboard=True
)
