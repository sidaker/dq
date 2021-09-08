FROM python:3.8.6

WORKDIR /app

COPY requirements/*.txt /app/requirements/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements/prod.txt

COPY newpipeline/*.py /app/newpipeline/
COPY newpipeline/fetcher/ /app/newpipeline/fetcher/
COPY newpipeline/normaliser/ /app/newpipeline/normaliser/

ENTRYPOINT ["python", "-m", "newpipeline", "worker", "-l", "info"]
