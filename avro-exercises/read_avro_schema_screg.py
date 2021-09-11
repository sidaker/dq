from schema_registry.client import SchemaRegistryClient, schema
## Needs testing

client = SchemaRegistryClient(url="http://127.0.0.1:8081")

deployment_schema = {
    "type": "record",
    "namespace": "com.kubertenes",
    "name": "AvroDeployment",
    "fields": [
        {"name": "image", "type": "string"},
        {"name": "replicas", "type": "int"},
        {"name": "port", "type": "int"},
    ],
}

avro_schema = schema.AvroSchema(deployment_schema)

schema_id = client.register("test-deployment", avro_schema)
