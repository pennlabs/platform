FROM python:3
ADD . /
WORKDIR /
RUN pip install pipenv
RUN pipenv install
RUN python manage.py collectstatic --noinput
