# app.py
import faust


VERSION = 1

PROJECT = "kafkaavropipe"  # our root directory
ORIGIN = "newpipeline"  # our app directory

AUTODISCOVER = [
    f"{ORIGIN}.fetcher",
    f"{ORIGIN}.normaliser",
]

BROKER = "kafka://broker:9092"

app = faust.App(
    PROJECT,
    version=VERSION,
    autodiscover=AUTODISCOVER,
    origin=ORIGIN,
    broker=BROKER,
)


def main() -> None:
    # HACK:
    # Waiting for kafka to be ready.
    # In production, you would add a wait script to your docker-compose
    # to make sure that kafka is ready when Faust starts.
    import time; time.sleep(60)

    app.main()
