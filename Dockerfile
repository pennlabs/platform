FROM python:3
ADD . /
WORKDIR /
RUN pip install pipenv
RUN pipenv install
RUN pipenv run python manage.py collectstatic --noinput
