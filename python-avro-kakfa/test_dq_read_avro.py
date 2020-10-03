# Python 3 with `avro-python3` package available
import copy
import json
import avro
from avro.datafile import DataFileWriter, DataFileReader
from avro.io import DatumWriter, DatumReader

#schema = avro.schema.parse(open("user.avsc", "rb").read())


# Read data from an avro file
with open('/Users/sbommireddy/Downloads/noprod_api_kafka_msg.json', 'rb') as f:
    reader = DataFileReader(f, DatumReader())
    metadata = copy.deepcopy(reader.meta)
    schema_from_file = json.loads(metadata['avro.schema'])
    users = [api for api in reader]
    reader.close()




print(f'Schema from users.avro file:\n {schema_from_file}')
print(f'Users:\n {users}')
