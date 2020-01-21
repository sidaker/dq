FROM python:3.7

WORKDIR /APP

RUN mkdir -p /APP/src

COPY src/ /APP/src/

RUN chmod +x src/app.py

RUN pip install --upgrade pip

RUN pip install flask

CMD python3 src/app.py
