FROM python:3.13-alpine AS base

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev cargo

RUN pip install "poetry==2.1.3"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
        && poetry install --no-interaction --no-ansi --no-root --without dev

FROM python:3.13-alpine AS dev

# Create a non-root user
ARG USERNAME=appuser
ARG USER_UID=1000
ARG USER_GID=1000

COPY --from=BASE /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=BASE /usr/local/bin/ /usr/local/bin/

# Create a group and user
RUN addgroup -g $USER_GID $USERNAME \
    && adduser -D -u $USER_UID -G $USERNAME $USERNAME

# Set the user home directory and copy application code
WORKDIR /project
COPY pyproject.toml poetry.lock ./
COPY app ./app
COPY  main.py .
COPY alembic.ini .
COPY alembic ./alembic

# Change ownership of the app directory to the non-root user
RUN chown -R $USERNAME:$USERNAME /project

# Switch to the non-root user
USER $USERNAME

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#ENTRYPOINT exec tail -f /dev/null
