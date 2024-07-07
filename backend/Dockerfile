FROM pennlabs/shibboleth-sp-nginx:3.0.4

LABEL maintainer="Penn Labs"

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /app/

# Update PGP key for NGINX
# https://blog.nginx.org/blog/updating-pgp-key-for-nginx-software
RUN wget -O/etc/apt/trusted.gpg.d/nginx.asc https://nginx.org/keys/nginx_signing.key

# Install dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y python3.11-dev pipenv python3-distutils libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy config files
COPY docker/shibboleth/ /etc/shibboleth/
COPY docker/nginx-default.conf /etc/nginx/conf.d/default.conf
COPY docker/shib_clear_headers /etc/nginx/
COPY docker/supervisord.conf /etc/supervisor/

# Copy project dependencies
COPY Pipfile* /app/

# Install project dependencies
RUN pipenv install --deploy --system

# Copy project files
COPY . /app/

ENV DJANGO_SETTINGS_MODULE Platform.settings.production
ENV SECRET_KEY 'temporary key just to build the docker image'
ENV IDENTITY_RSA_PRIVATE_KEY 'temporary private key just to build the docker image'

# Collect static files
RUN python3 /app/manage.py collectstatic --noinput

# Copy mime definitions
COPY docker/mime.types /etc/mime.types

# Copy start script
COPY docker/platform-run /usr/local/bin/

CMD ["platform-run"]
