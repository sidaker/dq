import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

schemafilepath='/Users/sbommireddy/Documents/python/assignments/dq/avro-exercises/schemas/user_1.avsc'
'''
Do make sure that you open your files in binary mode (i.e. using the modes wb or rb respectively).
Otherwise you might generate corrupt files due to automatic replacement of newline characters with
the platform-specific representations.
'''

'''
avro.schema.parse takes a string containing a JSON schema definition as input and outputs a avro.schema.Schema object
(specifically a subclass of Schema, in this case RecordSchema).
'''
schema = avro.schema.parse(open(schemafilepath, "rb").read())
print(schema)
print(type(schema))

'''
We create a DataFileWriter, which we'll use to write serialized items to a data file on disk.
The DataFileWriter constructor takes three arguments.
A DatumWriter, which is responsible for actually serializing the items to Avro's binary format
(DatumWriters can be used separately from DataFileWriters, e.g., to perform IPC with Avro).
'''
writer = DataFileWriter(open("users.avro", "wb"), DatumWriter(), schema)

#  Avro records are represented as Python dicts.
writer.append({"name": "Alyssa", "favorite_number": 256})
writer.append({"name": "Ben", "favorite_number": 7, "favorite_color": "red"})
writer.append({"name": "Advik", "favorite_number": 6, "favorite_color": "green"})
writer.close()

'''
The DataFileReader is an iterator that returns dicts corresponding to the serialized items.
'''
reader = DataFileReader(open("users.avro", "rb"), DatumReader())
for user in reader:
    print(user)
reader.close()
