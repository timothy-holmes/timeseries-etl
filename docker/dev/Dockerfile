FROM python:3.11 as pip_compile

WORKDIR /app
COPY pyproject.toml pyproject.toml
RUN pip install pip-tools
RUN pip-compile --extra dev -o dev-requirements.txt pyproject.toml
RUN pip-compile -o requirements.txt pyproject.toml

# install project deps (standard)
FROM python:3.11 as base

WORKDIR /app

# copy requirements.txt and install via pip 
COPY --from=pip_compile /app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# install extra dev deps
FROM base as dev

# copy extra requirements.txt and install via pip 
COPY --from=pip_compile /app/dev-requirements.txt dev-requirements.txt
RUN pip install -r dev-requirements.txt

# add required creds
ARG TAPO_PASS
ENV TAPO_PASSWORD=$TAPO_PASS

### dev/prod Dockerfile, same to here