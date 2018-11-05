FROM python:3
ADD . /
WORKDIR /
ADD requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 5000
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "-b", "0.0.0.0:5000", "pennlabs.wsgi"]