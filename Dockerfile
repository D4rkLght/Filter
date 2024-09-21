###############################################
# Base Stage
###############################################
FROM python:3.11-slim as base

ARG APP_SERVICE_HOSTNAME \
    APP_WSGI_HOST \
    APP_WSGI_PORT \
    APP_WSGI_RELOAD \
    APP_WSGI_WORKERS \
    APP_DOCS_USERNAME\
    APP_TELEGRAM_TOKEN \
    APP_LOG_LEVEL \
    APP_WEBHOOK_MODE \
    APP_WEBHOOK_PATH \
    APP_WEBHOOK_URL \
    APP_TELEGRAM_USER_ID

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    APP_SERVICE_HOSTNAME=${APP_SERVICE_HOSTNAME} \
    APP_WSGI_APP_PATH=${APP_WSGI_APP_PATH:-bot.main:app} \
    APP_WSGI_HOST=${APP_WSGI_HOST:-0.0.0.0} \
    APP_WSGI_PORT=${APP_WSGI_PORT:-80} \
    APP_WSGI_RELOAD=${APP_WSGI_RELOAD:-false} \
    APP_WSGI_WORKERS=${APP_WSGI_WORKERS:-1} \
    APP_TELEGRAM_TOKEN=${APP_TELEGRAM_TOKEN} \
    APP_LOG_LEVEL=${APP_LOG_LEVEL} \
    APP_WEBHOOK_MODE=${APP_WEBHOOK_MODE} \
    APP_WEBHOOK_PATH=${APP_WEBHOOK_PATH} \
    APP_WEBHOOK_URL=${APP_WEBHOOK_URL} \
    APP_TELEGRAM_USER_ID=${APP_TELEGRAM_USER_ID}

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

###############################################
# Build Stage
###############################################
FROM base as build

# RUN sed -i -e 's/http:\/\/deb\.debian\.org\/debian/http:\/\/mirror\.yandex\.ru\/debian/g' /etc/apt/sources.list

RUN BUILD_DEPS="build-essential libpq-dev curl" \
    && apt-get update \
    && apt-get install --no-install-recommends -y $BUILD_DEPS \
    && apt-get clean all

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python - \
    && chmod a+x "$POETRY_HOME/bin/poetry"

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --only main --no-root --verbose

###############################################
# Development Stage
###############################################
FROM base as development

ARG USER_UID \
    USER_GID

ENV USER_UID=${USER_UID:-1500} \
    USER_GID=${USER_GID:-1500} \
    APP_ENVIRONMENT=development

COPY --from=build $PYSETUP_PATH $PYSETUP_PATH
COPY --from=build $POETRY_HOME $POETRY_HOME
COPY --from=build $VENV_PATH $VENV_PATH

COPY ./docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh
RUN groupadd -g $USER_GID bot \
    && useradd -m -u $USER_UID -g bot bot

WORKDIR $PYSETUP_PATH
RUN poetry install --no-root --verbose

COPY --chown=bot:bot . /workspace
USER bot
WORKDIR /workspace/

EXPOSE 5050
ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD ["uvicorn", "bot.main:app", "--reload", "--host=0.0.0.0", "--port=5050"]
