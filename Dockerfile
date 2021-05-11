FROM python:3

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY ./main.py /usr/src/app
COPY ./process.py /usr/src/app
COPY ./videoProcessor.py /usr/src/app
COPY ./imports /usr/src/app
COPY ./exports /usr/src/app
COPY ./data /usr/src/app

ENV PORT 5000

EXPOSE $PORT

CMD [ "python", "./main.py" ]