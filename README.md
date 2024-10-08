![filter_workflow](https://github.com/D4rkLght/Filter/actions/workflows/Deploy.yml/badge.svg)
# Filter
Filter telegram bot

Бот для предоставления услуг по изучению английского языка.

# Содержание

1. [Cведения о команде](#info)
2. [Cсылка на бота](#host)
3. [Подготовка к запуску](#start)

    3.1. [Правила работы с git](#git)

    3.2. [Настройка переменных окружения](#env)

    3.3. [Запуск бота локально](#local)

4. [Cтэк технологий](#stack)


# 1. Cведения о команде: <a id="info"></a>

1. Разработчик [Ярослав Андреев ](https://github.com/D4rkLght)

# 2. Cсылка на бота <a id="host"></a>

[Бот](http://t.me/valeriestill_bot)

# 3. Подготовка к запуску <a id="start"></a>

Примечание: использование Docker, poetry.

## 3.1. Правила работы с git (как делать коммиты и pull request-ы)<a id="git"></a>:

1. Две основные ветки: `main` и `develop`
2. Ветка `develop` — “предрелизная”. Т.е. здесь должен быть рабочий и выверенный код
3. Создавая новую ветку, наследуйтесь от ветки `develop`
4. В `main` находится только production-ready код (CI/CD)
5. Правила именования веток
   - весь новый функционал — `feature/название-функционала`
   - исправление ошибок — `bugfix/название-багфикса`
6. Пушим свою ветку в репозиторий и открываем Pull Request


## 3.2. Настройка переменных окружения <a id="env"></a>

Перед запуском проекта необходимо создать копию файла
```.env.example```, назвав его ```.env``` и установить значение базы данных почты и тд.

### Системные требования
- Python 3.11+;
- Docker (19.03.0+) c docker compose;
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer);

Установка зависимостей poetry:

```shell
poetry install
```

## 3.3. Запуск бота локально <a id="local"></a>

Запуск сервера локально:

запуск бота с использованием докера:
```shell
make bot-start
```

запуск бота без докера:
```shell
make bot-init
```

пересборка докера:
```shell
make bot-reb
```

удаление докер контейнера:
```shell
docker bot-delete
```


# 4 Cтэк технологий <a id="stack"></a>

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/ru/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Poetry](https://img.shields.io/badge/Poetry-808080?style=for-the-badge&logo=Poetry)](https://python-poetry.org/)
