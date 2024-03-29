from avro.schema import parse
from avro.datafile import DataFileWriter
from avro.io import DatumWriter


class AvroWriter:
    def __init__(self, avro_schema_file, avro_data_file):
        self.avro_data_file = avro_data_file
        self.schema = parse(open(avro_schema_file, "rb").read())

    def write_sample(self):
        with DataFileWriter(open(self.avro_data_file, "wb"),
                            DatumWriter(),
                            self.schema) as writer:
            writer.append({'name': 'Prague',
                           "year": 2020,
                           "population": 1324277,
                           "area": 496})
            writer.append({'name': 'Berlin',
                           "year": 2019,
                           "population": 3769495,
                           "area": 891})
            writer.append({'name': 'London',
                           "year": 2021,
                           "population": 5769495,
                           "area": 655})
            writer.append({'name': 'Vienna',
                           "year": 2018,
                           "population": 1888776,
                           "area": 414})
