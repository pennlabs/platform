FROM pennlabs/shibboleth-sp-nginx

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Install dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y python3.7-dev python3-distutils default-libmysqlclient-dev gcc \
    && wget -qO get-pip.py "https://github.com/pypa/get-pip/raw/0c72a3b4ece313faccb446a96c84770ccedc5ec5/get-pip.py" \
    && python3.7 get-pip.py \
        --disable-pip-version-check \
        --no-cache-dir \
    && pip3 install pipenv \
    && rm -f get-pip.py \
    && rm -rf /var/lib/apt/lists/*

# Copy config files
COPY docker/shibboleth/ /etc/shibboleth/
COPY docker/nginx-default.conf /etc/nginx/conf.d/default.conf
COPY docker/shib_clear_headers /etc/nginx/
COPY docker/supervisord.conf /etc/supervisor/

# Copy platform dependencies
COPY Pipfile* /app/

# Install platform dependencies
WORKDIR /app/
RUN pipenv install --system

# Copy platform
COPY . /app/

# Collect static files
RUN python3.7 /app/manage.py collectstatic

# Copy start script
COPY docker/platform-run /usr/local/bin/

CMD ["platform-run"]