ARG PYTHON_VERSION=3.9.9-bullseye
ARG DEV=false


FROM python:${PYTHON_VERSION} AS builder
ARG DEV
ARG POETRY_VERSION=1.1.12

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install -qq "poetry==$POETRY_VERSION"

RUN python -m venv /venv

COPY ./pyproject.toml ./poetry.lock ./

RUN echo $DEV
RUN /bin/bash -c 'poetry export $(test "$DEV" == true && echo "--dev") | /venv/bin/pip install --no-deps -r /dev/stdin'


FROM python:$PYTHON_VERSION

ENV PYTHONUNBUFFERED 1

COPY --from=builder /venv /venv

RUN groupadd django && useradd -g django -s /bin/sh django

COPY ./compose/django/entrypoint /entrypoint
COPY ./compose/django/health.py /health
COPY ./compose/django/runserver /runserver
COPY ./compose/django/gunicorn /gunicorn
COPY ./compose/django/migrate /migrate
COPY ./compose/django/celeryworker /celeryworker
COPY ./compose/django/celerybeat /celerybeat
COPY ./compose/django/celeryflower /celeryflower

RUN chmod +x /entrypoint /health /runserver /gunicorn /migrate /celeryworker /celerybeat /celeryflower

COPY ./app /app
RUN chown -R django:django /app

WORKDIR /app
USER django

ENTRYPOINT ["/entrypoint"]
