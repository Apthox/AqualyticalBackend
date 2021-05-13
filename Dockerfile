FROM python:3

LABEL maintainer="Kevin Guzman <keguzman@csumb.edu>"

COPY ./requirements.txt /app/requirements.txt

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app", "-w", "2", "--timeout", "120"]