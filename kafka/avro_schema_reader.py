import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter




if __name__ == "__main__":
    schema = avro.schema.parse(open("/Users/sbommireddy/Documents/python/assignments/dq/avro_test_schema.avsc").read())
    #schema1 = avro.schema.parse(open("/Users/sbommireddy/Documents/python/assignments/dq/test2avro.avsc" , "rb").read())
    print(schema,  sep="---")
    #print(schema1)
