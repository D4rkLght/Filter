from telegram.constants import ParseMode
from telegram.ext import CallbackContext

from bot.logging.logging import debug_logger
from bot.constants.messages import TIME_LONG_MESSAGE
from bot.keyboards.conversation_keyboards import message_long_time_keyboard_markup
from bot.constants.states import States


@debug_logger
async def send_message(context: CallbackContext) -> None:
    """Отправляет сообщение если пользователь не произвёл транзакцию."""
    if context.job:
        await context.bot.send_message(
            chat_id=context.job.user_id,
            text=TIME_LONG_MESSAGE,
            reply_markup=message_long_time_keyboard_markup,
            parse_mode=ParseMode.HTML,
        )
