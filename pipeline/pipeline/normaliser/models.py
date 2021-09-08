# normaliser/models.py
import faust

from pipeline.app import app


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


input_schema = faust.Schema(
    key_type=str,
    value_type=RawUser,
    key_serializer="json",
    value_serializer="json",
)

input_topic = app.topic("fetcher-0.0.1", schema=input_schema)


class NormalisedUser(faust.Record):
    id: str
    name: str
    cell: str
    email: str


output_schema = faust.Schema(
    key_type=str,
    value_type=NormalisedUser,
    key_serializer="json",
    value_serializer="json",
)

output_topic = app.topic("normaliser-0.0.1", schema=output_schema)
