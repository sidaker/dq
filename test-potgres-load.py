import psycopg2

conn = psycopg2.connect("dbname=animal_shelter user=postgres password=postgres")
conn_parameters = {
            'host': '',
            'dbname': '',
            'user': '',
            'password': '',
            'options': '-c statement_timeout=60000'
        }


##conn = psycopg2.connect(**conn_parameters)
## copy_sql = "copy {0}.{1} FROM STDIN WITH CSV delimiter ',' HEADER;".format(target_schema, target_table)
copy_sql = "copy public.stg_tbl_api FROM STDIN WITH CSV delimiter ',' HEADER;"
file =  '/Users/sbommireddy/Downloads/api.csv'
file_obj = open(file, 'rb')

for lineno, line in enumerate(file_obj):
    pass

records_in_file = lineno+1
header = True
cur = conn.cursor()
if header:
    records_in_file = records_in_file-1
    file_obj.seek(0)
    print("Copying to table")
    records_loaded = cur.rowcount
    print(records_loaded)
    cur.copy_expert(copy_sql, file_obj)
    records_loaded = cur.rowcount
    print(records_loaded)
    file_obj.close()
    conn.commit()
    cur.close()
