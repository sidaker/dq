# normaliser/models.py
import faust
import avro
from avro.schema import parse
import json
from faust_avro_serializer import FaustAvroSerializer
from schema_registry.client import SchemaRegistryClient
from newpipeline.app import app
from schema_registry.client import SchemaRegistryClient, schema


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

user_avro_schema = avro.schema.parse(json.dumps({
"namespace": "org.example.avro",
"type": "record",
"name": "NormalisedUser",
"fields": [
  {"name": "id", "type": "string"},
  {"name": "name", "type": "string"},
  {"name": "cell", "type": "string"},
  {"name": "email", "type": "string"}
]
}))

#user_avro_schema = schema.AvroSchema(avro_schema_raw)
#client = SchemaRegistryClient("http://my-schema-registry:8081")
#serializer = FaustAvroSerializer(client, my_topic_name, False)
#schema_with_avro = Schema(key_serializer=str, value_serializer=serializer)
#dummy_topic = app.topic(my_topic_name, schema=schema_with_avro)
user_avro_serializer = FaustSerializer(schema_registry_client,'NormalisedUser',user_avro_schema)

class NormalisedUser(faust.Record, serializer=user_avro_serializer):
    id: str
    name: str
    cell: str
    email: str


output_schema = faust.Schema(
    key_type=str,
    value_type=NormalisedUser,
    key_serializer="json",
    value_serializer=user_avro_serializer,
)

output_topic = app.topic("normaliser-0.0.1", schema=output_schema)
