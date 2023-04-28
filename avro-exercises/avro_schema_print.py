import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

schema = avro.schema.parse(open("api.avsc","rb").read())
print(schema)
schema_1=schema.meta
print(schema_1)

schema = avro.schema.parse(open("apiv2.avsc","rb").read())
schema_2=schema.meta
print(schema_2)
