import psycopg2

'''
python /Users/sbommireddy/Documents/python/assignments/dq/python/postgres-3.py
'''

conn = psycopg2.connect("dbname=learning user=sid")
cur = conn.cursor()
#cur.execute("""SELECT * FROM  users""")
insert_query = "INSERT INTO users VALUES {}".format("(10, 'hello@dadvitek.io', 'Some Name', '123 Fake St.')")
cur.execute(insert_query)
cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s)", (20, 'hello@dadvitek.io', 'Sid', 'Great Street St.'))
'''
This type of insert automatically converts each one of the types to the proper datatype expected by the table.
Another benefit is that your insert queries are actually sped up since the INSERT statement is prepared in the database. 
'''
conn.commit()
