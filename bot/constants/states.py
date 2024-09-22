import enum


class States(str, enum.Enum):
    """Класс, описывающий состояния бота."""

    GO = "go"
    CHOOSE = "choose"
    SCREEN = "screen"
    END = "end"
    HELP = "help"
