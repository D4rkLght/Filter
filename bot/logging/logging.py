import sys

from loguru import logger


def setup_logger(logger_level: str):
    """Функция для настройки логгера."""
    logger.remove(0)
    logger.level("DEBUG", color="<yellow>")
    logger.add(
        sys.stdout,
        level=logger_level,
        backtrace=True,
        diagnose=True,
    )
    logger.add(
        "./logs/{time:YYYY-MM-DD}.log",
        rotation="1 month",
        level=logger_level,
        backtrace=True,
        diagnose=True,
    )


def debug_logger(func):
    """Декоратор для логирования обработчиков и шедулеров."""
    schedulers_data = [
        "send_message",
    ]

    async def wrapper(*args, **kwargs):
        if func.__name__ in schedulers_data:
            context = args[0] if args else kwargs.get("context")
            job = context.job if context else None
            user_id = job.user_id if job else "Unknown"
            username = job.name if job.name else "Unknown"
            func_type = "Scheduler"
        else:
            update = args[0] if args else kwargs.get("update")
            user = update.effective_user if update else None
            func_type = "Handler"
            user_id = user.id if user else "Unknown"
            username = user.username if user else "Unknown"
        try:
            result = await func(*args, **kwargs)
            logger.debug(
                f"User: {username} (ID: {user_id}) | " f"{func_type}: {func.__name__}"
            )
            return result
        except Exception as e:
            logger.exception(
                f"User: {username} "
                f"(ID: {user_id}) | "
                f"{func_type}: {func.__name__} | "
                f"Exception: {e}"
            )
            raise e

    return wrapper
