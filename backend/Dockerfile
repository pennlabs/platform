FROM pennlabs/shibboleth-sp-nginx:3.0.4

LABEL maintainer="Penn Labs"

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /app/

# Install dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y python3.11-dev python3-distutils libpq-dev gcc python3.11-venv \
    && python3.11 -m venv /opt/venv

# Activate virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Install pipenv using pip
RUN pip install --upgrade pip \
    && pip install pipenv

# Clean up
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy config files
COPY docker/shibboleth/ /etc/shibboleth/
COPY docker/nginx-default.conf /etc/nginx/conf.d/default.conf
COPY docker/shib_clear_headers /etc/nginx/
COPY docker/supervisord.conf /etc/supervisor/

# Copy project dependencies
COPY Pipfile* /app/

# Install project dependencies
RUN pipenv install --system

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
