from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)

from bot.constants.buttons import (BACK_BUTTON, CARD_BUTTON, CRYPTO_BUTTON,
                                   HELP_BUTTON, PRIVATE_BUTTON, RESTART_BUTTON,
                                   TELEGRAM_BUTTON)

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

choose_pay_keyboard_markup = ReplyKeyboardMarkup([
    [
        CRYPTO_BUTTON
    ],
    [
        CARD_BUTTON
    ]], resize_keyboard=True
)

message_long_time_keyboard_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text=TELEGRAM_BUTTON, url="https://t.me/valeriestill"),
            InlineKeyboardButton(text=PRIVATE_BUTTON, url="https://t.me/tribute/app?startapp=sfzP"),
        ],
        [
            InlineKeyboardButton(text=HELP_BUTTON, url="https://t.me/v_still_manager"),
            InlineKeyboardButton(text=RESTART_BUTTON, callback_data='start'),
        ]
    ]
)

remove_keyboard_markup = ReplyKeyboardRemove(True)
