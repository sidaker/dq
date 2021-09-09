from avro.schema import parse



class AvroSchemaParser:
    def __init__(self, avro_schema_file):
        self.schema = parse(open(avro_schema_file, "rb").read())

    def printshow(self):
        # There is schema available in meta field
        print("---- SCHEMA ----")
        # Print schema as dict
        print(self.schema)
        for i in self.schema.fields:
            print(i.name)
            #print(dir(i))
            #print(type(i))
            #<class 'avro.schema.Field'>loo


if __name__ == '__main__':
    #schfile='/Users/sbommireddy/Documents/python/assignments/dq/avro-exercises/schemas/avro_schemas_consumer_schema_cdlz_seacontainer_manifests.avsc'
    schfile='/Users/sbommireddy/Documents/python/assignments/dq/avro-exercises/schemas/city.avsc'
    schema_parsed = AvroSchemaParser(schfile)
    print(dir(schema_parsed))
    print(schema_parsed.printshow())
    print("*****")
