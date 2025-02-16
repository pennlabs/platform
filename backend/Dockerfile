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

# Install uv
# Download the latest installer
ADD https://astral.sh/uv/0.6.0/install.sh /uv-installer.sh

RUN echo "5464b06094b6363861b99cd60a010892e52fc2a7503b7594419828e74afecfe6  /uv-installer.sh" | sha256sum -c

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

#RUN curl -LsSf https://astral.sh/uv/0.4.30/install.sh | sh

# Copy config files
COPY docker/shibboleth/ /etc/shibboleth/
COPY docker/nginx-default.conf /etc/nginx/conf.d/default.conf
COPY docker/shib_clear_headers /etc/nginx/
COPY docker/supervisord.conf /etc/supervisor/

# Copy project dependencies
COPY pyproject.toml /app/
COPY uv.lock /app/

# Install project dependencies
RUN cd /app/ && uv sync

# Copy project files
COPY . /app/

ENV DJANGO_SETTINGS_MODULE Platform.settings.production
ENV SECRET_KEY 'temporary key just to build the docker image'
ENV IDENTITY_RSA_PRIVATE_KEY 'temporary private key just to build the docker image'
ENV OIDC_RSA_PRIVATE_KEY 'temporary private key just to build the docker image'

# Collect static files
RUN uv run /app/manage.py collectstatic --noinput

# Copy mime definitions
COPY docker/mime.types /etc/mime.types

# Copy start script
COPY docker/platform-run /usr/local/bin/

CMD ["platform-run"]
