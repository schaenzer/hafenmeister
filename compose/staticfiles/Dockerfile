ARG DJANGO_IMAGE
ARG NGINX_VERSION=1.21.0


FROM ${DJANGO_IMAGE} AS builder

USER root
RUN /entrypoint python manage.py collectstatic --noinput --settings=config.settings.base


FROM nginxinc/nginx-unprivileged:${NGINX_VERSION}

COPY ./compose/staticfiles/nginx-default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /staticfiles/ /var/www/static
