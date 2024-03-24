ARG tapo_password

# get two sets of deps in requirements.txt format
FROM python:3.11 as pip_compile


WORKDIR /app
COPY pyproject.toml pyproject.toml
RUN pip install pip-tools
RUN pip-compile --extra dev -o dev-requirements.txt pyproject.toml
RUN pip-compile -o requirements.txt pyproject.toml

# install project deps (standard)
FROM python:3.11 as base
ENV TAPO_PASSWORD $tapo_password

WORKDIR /app
COPY --from=pip_compile /app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# install extra dev deps
FROM base as tests
ENV TAPO_PASSWORD $tapo_password

COPY --from=pip_compile /app/dev-requirements.txt dev-requirements.txt
RUN pip install -r dev-requirements.txt

# same as prod Dockerfile to here
