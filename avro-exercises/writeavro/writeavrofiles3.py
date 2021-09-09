from avro.schema import parse
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import os


class AvroS3Writer:
    def __init__(self, avro_schema_file, avro_data_file):
        self.avro_data_file = avro_data_file
        self.schema = parse(open(avro_schema_file, "rb").read())

    def upload_to_aws(self,local_file, bucket, s3_file):
        s3 = boto3.client('s3')

        try:
            s3.upload_file(local_file, bucket, s3_file)
            print(f"Upload of file {local_file} Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False


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
            writer.append({'name': 'Vienna',
                           "year": 2018,
                           "population": 1888776,
                           "area": 414})
