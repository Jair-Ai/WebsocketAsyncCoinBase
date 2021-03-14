# 1. Base image
FROM python:3.8.3-slim-buster

# 👇 python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.0.10 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'


# 👇
ENV TINI_VERSION="v0.19.0"

# 👇
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
# 👆


# 👇 Updating some python packages
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential python3-dev python3-setuptools musl-dev wget git libpq-dev \
    && pip install "poetry==$POETRY_VERSION" && poetry --version

# 👇
WORKDIR /project

# 👇 Not using root to run software
RUN useradd -m -r user && \
    chown user /project

# 👇
COPY . .

# 👇
ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}
# 👆


# 👇 here we set the user
USER user


# 👇
RUN poetry install --no-interaction --no-ansi


# 👇 Using tini to run software
ENTRYPOINT ["/tini", "--"]


CMD ["/coinbasewebsocke/async_websocket.py"]