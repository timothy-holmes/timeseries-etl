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
# dev/prod Dockerfile, same to here

FROM base as staging
ARG TAPO_PASS
ENV TAPO_PASSWORD $TAPO_PASS

WORKDIR /app
COPY ./src src
COPY ./config config


# install extra dev deps
FROM staging as tests

COPY --from=pip_compile /app/dev-requirements.txt dev-requirements.txt
RUN pip install -r dev-requirements.txt

ARG TAPO_PASS
ENV TAPO_PASSWORD=$TAPO_PASS

ARG R
WORKDIR /app
COPY ./pyproject.toml pyproject.toml
COPY ./tests tests

# run tests (additional parameters required for long-running tests)
# arg R is random number to block caching pytest
RUN pytest --longtest --outside


FROM staging as prod
ARG R
ARG TAPO_PASS
ENV TAPO_PASSWORD $TAPO_PASS