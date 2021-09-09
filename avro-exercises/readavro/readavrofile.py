from avro.schema import parse
from avro.datafile import DataFileReader
from avro.io import DatumReader
import json
import pandas as pd

class AvroReader:
    def __init__(self, data_file):
        self.avro_reader = DataFileReader(open(data_file, "rb"),
                                          DatumReader())

    def print(self):
        # There is schema available in meta field
        print("---- SCHEMA ----")
        # Print schema as dict
        print(self.avro_reader.meta)
        # Or load it into json
        schema_json = json.loads(self.avro_reader.meta.get('avro.schema').decode('utf-8'))
        print('Avro schema [{}]: {}.{}'.format(schema_json['type'], schema_json['namespace'], schema_json['name']))

        for field in schema_json['fields']:
            print('{}:{}'.format(field['name'], field['type']))
        records = [record for record in self.avro_reader]
        print("---- AVRO RECORDS ----")
        print(records)
        print("---- PANDAS DATAFRAME ----")
        print(pd.DataFrame.from_records(records))
