from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)

from bot.constants.buttons import (BACK_BUTTON, CARD_BUTTON, CRYPTO_BUTTON,
                                   HELP_BUTTON)

back_keyboard_markup = ReplyKeyboardMarkup([
    [
        BACK_BUTTON
    ],
    [
        HELP_BUTTON
    ]
    ], resize_keyboard=True
)

choose_pay_keyboard_markup = ReplyKeyboardMarkup([
    [
        CRYPTO_BUTTON
    ],
    [
        CARD_BUTTON
    ]], resize_keyboard=True
)

remove_keyboard_markup = ReplyKeyboardRemove(True)
