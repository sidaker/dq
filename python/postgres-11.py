import psycopg2
import csv
import sys
import gzip



conn = psycopg2.connect("dbname=learning user=sid")
cur = conn.cursor()
table_name='stg_flightstats'

file='/Users/sbommireddy/Desktop/code/20201110_test.gz'
gzfile = gzip.open(file, 'rb')
gzfile.seek(0)
cur.copy_expert("copy public.{0} FROM STDIN WITH CSV delimiter E'\001'".format(table_name) + r''' QUOTE E'\b' null '\N';''', gzfile)
records_loaded = cur.rowcount
print('Loaded %s records (prior to commit)', cur.rowcount)
gzfile.close()


conn.commit()
print('Committed.')
cur.close()

conn.close()
