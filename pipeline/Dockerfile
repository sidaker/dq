FROM python:3.8.6

WORKDIR /app

COPY requirements/*.txt /app/requirements/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements/prod.txt

COPY pipeline/*.py /app/pipeline/
COPY pipeline/fetcher/ /app/pipeline/fetcher/
COPY pipeline/normaliser/ /app/pipeline/normaliser/

ENTRYPOINT ["python", "-m", "pipeline", "worker", "-l", "info"]
