from readavro import readavrofile
from writeavro import writeavrofile

avsch_file = '/Users/sbommireddy/Documents/python/assignments/dq/avro-exercises/schemas/city.avsc'
avdata_file='/Users/sbommireddy/Documents/python/assignments/dq/avro-exercises//data/city.avro'
avwriterobj = writeavrofile.AvroWriter(avsch_file,avdata_file)
avwriterobj.write_sample()
avreaderobj = readavrofile.AvroReader(avdata_file)
avreaderobj.print()
