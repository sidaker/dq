# normaliser/agents.py
import logging

from pipeline.app import app
from .models import input_topic, output_topic


logger = logging.getLogger(__name__)


def normalise_user(raw_user):
    return {
        "id": raw_user["id"]["value"],
        "name": f"{raw_user['name']['first']} {raw_user['name']['last']}",
        "cell": raw_user["cell"],
        "email": raw_user["email"],
    }


@app.agent(input_topic)
async def consume(stream):
    async for record in stream:
        raw_user = record.asdict()

        normalised_user = normalise_user(raw_user)
        key = normalised_user["id"]

        logger.info("Normalised user with ID %(user_id)s", {"user_id": key})

        await output_topic.send(key=key, value=normalised_user)
