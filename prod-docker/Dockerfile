# get two sets of deps in requirements.txt format
FROM python:3.11 as pip_compile

WORKDIR /app
COPY pyproject.toml pyproject.toml
RUN pip install pip-tools
RUN pip-compile --extra dev -o dev-requirements.txt pyproject.toml
RUN pip-compile -o requirements.txt pyproject.toml

# install project deps (standard)
FROM python:3.11 as base

WORKDIR /app
COPY --from=pip_compile /app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# install extra dev deps, copy src and tests, run pytest
FROM base as tests

COPY --from=pip_compile /app/dev-requirements.txt dev-requirements.txt
RUN pip install -r dev-requirements.txt

WORKDIR /app
COPY ./config config
COPY ./src src
COPY ./tests tests

RUN pytest

# copy src
FROM base as prod

WORKDIR /app
COPY ./src src
COPY ./config config
