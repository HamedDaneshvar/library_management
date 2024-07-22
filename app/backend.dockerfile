FROM python:3.10

WORKDIR /app/
ENV PYTHONPATH=/app

# Install necessary packages
RUN apt-get update && apt-get install -y netcat-openbsd

# Install Poetry version 1
RUN pip install poetry fastapi uvicorn
RUN poetry config virtualenvs.create false
# Copy poetry.lock* in case it doesn't exist in the repo
COPY . /app/
RUN poetry export -f requirements.txt --without-hashes --output /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
