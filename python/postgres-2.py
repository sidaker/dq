import psycopg2

'''
python /Users/sbommireddy/Documents/python/assignments/dq/python/postgres-2.py
'''

conn = psycopg2.connect("dbname=learning user=sid")
cur = conn.cursor()
cur.execute("""CREATE TABLE users(
    id integer PRIMARY KEY,
    email text,
    name text,
    address text
)
""")
conn.commit()
