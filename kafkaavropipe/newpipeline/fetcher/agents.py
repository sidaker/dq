# fetcher/agents.py
import logging

import pytz
import requests

from newpipeline.app import app
from .models import output_topic


logger = logging.getLogger(__name__)


@app.crontab("*/5 * * * *", timezone=pytz.timezone("US/Eastern"), on_leader=True)
async def fetch():
    response = requests.get("https://randomuser.me/api/?results=50")
    response.raise_for_status()

    data = response.json()
    for result in data["results"]:
        key = result["id"]["value"]
        if not key:
            # randomuser.me has some some users with None or empty ID value,
            # we don't want to process these.
            continue

        logger.info("Fetched user with ID %(user_id)s", {"user_id": key})

        await output_topic.send(key=key, value=result)
