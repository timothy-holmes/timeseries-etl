FROM python:3.11

# install git
# (already installed) RUN apt-get update && apt-get install -y git
RUN git config --global --add safe.directory /app

# install dev dependencies
RUN pip install pytest pre-commit

CMD ["tail", "-f", "/dev/null"]
