FROM python:3
ADD . /
WORKDIR /
ADD requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "pennlabs.wsgi"]