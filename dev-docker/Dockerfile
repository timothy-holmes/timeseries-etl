FROM python:3.11

WORKDIR /app

# install git
# (already installed) RUN apt-get update && apt-get install -y git
RUN git config --global --add safe.directory /app

# install dev dependencies (doesn't work because volume is defined in docker-compose.yml)
# RUN pip install .[dev] && \
#     pip uninstall -y timeseries_etl

CMD ["tail", "-f", "/dev/null"]
