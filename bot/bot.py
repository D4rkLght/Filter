import asyncio
from typing import Self

from loguru import logger
from telegram import BotCommand
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from bot.handlers.command_handlers import (
    start,
    start_handler,
)
from bot.handlers.conversation_handlers import (
    pay,
    payment,
    end
)
from bot.constants.states import States

from bot.logging.logging import setup_logger
from bot.core.settings import settings


class Bot:
    """Класс-синглтон для управления телеграм-ботом."""

    _instance: Self | None = None

    def __new__(cls, *args, **kwargs):
        """Синглтон-конструктор."""
        if cls._instance is None:
            cls._instance = super(Bot, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Инициализация бота."""
        self._app: Application | None = None
        self._stop_event = asyncio.Event()
        logger.info("Bot instance created.")

    async def start(self) -> None:
        """Запускает бота."""
        logger.info("Bot starting...")
        self._stop_event.clear()
        asyncio.ensure_future(self._run(), loop=asyncio.get_event_loop())
        # task = asyncio.ensure_future(self._run(), loop=asyncio.get_event_loop())
        # await task

    def stop(self) -> None:
        """Останавливает бота."""
        logger.info("Bot stopping...")
        self._stop_event.set()

    async def _run(self) -> None:
        """Главный асинхронный метод, управляющий жизненным циклом бота."""
        self._app = await self._build_app()
        await self._app.initialize()
        await self._start_polling()
        await self.set_bot_commands()
        await self._start_bot()
        try:
            await self._stop_event.wait()
        except:
            await self._stop_bot()
            self.stop()

    async def _build_app(self) -> Application:
        """Создает и настраивает приложение для бота."""

        app = ApplicationBuilder().token(settings.app_settings.telegram_token).build()
        main_handler = await build_main_handler()
        app.add_handlers([main_handler, start_handler])
        return app

    async def _start_polling(self) -> None:
        """Polling started."""
        if settings.app_settings.webhook_mode:
            await self._app.bot.set_webhook(
                url=settings.app_settings.webhook_url,
                secret_token=settings.app_settings.webhook_secret_key,
                allowed_updates=["message", "callback_query"],
            )
            logger.info(f"Webhook set up at {settings.WEBHOOK_URL}")
        else:
            await self._app.bot.delete_webhook()
            await self._app.updater.start_polling()
            logger.info("Polling started")

    async def _start_bot(self) -> None:
        """Запускает основное приложение."""
        await self._app.start()

    async def _stop_bot(self) -> None:
        """Останавливает основное приложение."""
        await Application.stop(self._app)

    async def set_bot_commands(self) -> None:
        """Установить команды бота и их описание для кнопки Menu."""
        commands: list[BotCommand] = [
            BotCommand('start', 'start'),
        ]

        await self._app.bot.set_my_commands(commands)

    async def get_job_queue(self):
        """Функция получения job_queue."""
        return self._app.job_queue


async def build_main_handler():
    """Функция создания главного обработчика."""
    return ConversationHandler(
        entry_points=[start_handler],
        persistent=False,
        name="main_handler",
        states={
            States.GO: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, pay
                )
            ],
            States.CHOOSE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, payment
                )
            ],
            States.SCREEN: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, pay
                ),
                MessageHandler(
                    filters.PHOTO & ~filters.COMMAND, end
                ),
            ]
        },
        fallbacks=[start_handler],
    )

# async def main():
#     bot = Bot()
#     setup_logger(settings.app_settings.log_level)
#     await bot.start()

# if __name__ == "__main__":
#     asyncio.run(main())
