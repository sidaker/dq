import avro
from avro.schema import parse
import json


avro_schema_raw = {
  "namespace": "org.example.avro",
  "type": "record",
  "name": "NormalisedUser",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "name", "type": "string"},
    {"name": "cell", "type": "string"},
    {"name": "email", "type": "string"}
  ]
}


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

read_schema = avro.schema.parse(json.dumps({
"namespace": "example.avro",
"type": "record",
"name": "User",
"fields": [
    {"name": "first_name", "type": "string", "default": "", "aliases": ["name"]},
        {"name": "favorite_number", "type": ["int", "null"]},
        {"name": "favorite_color", "type": ["string", "null"]}
    ]
}))

#user_avro_schema = schema.AvroSchema(avro_schema_raw)
