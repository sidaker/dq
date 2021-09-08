# fetcher/models.py
import faust

from newpipeline.app import app


class RawUser(faust.Record):
    id: dict
    gender: str
    name: dict
    location: dict
    email: str
    login: dict
    dob: dict
    registered: dict
    phone: str
    cell: str
    picture: dict
    nat: str


output_schema = faust.Schema(
    key_type=str,
    value_type=RawUser,
    key_serializer="json",
    value_serializer="json",
)

output_topic = app.topic("fetcher-0.0.1", schema=output_schema)
