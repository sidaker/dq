import psycopg2
#import psycopg2
#conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")


conn = psycopg2.connect("host=localhost dbname=sbommireddy user=sbommireddy")
'''
connection to Postgres by using the connect() method of the psycopg2 module.
The connect() method takes in a sequence of parameters that the library uses to connect to the Postgres server.
The return value of the connect() method is a Connection object.
'''
cur = conn.cursor()
'''
The connection object creates a client session with the database server that instantiates a persistant client to speak with.
To issue commands against the database, you will also need to create another object called the Cursor object.
Cursor is created by the Connection object and using the Cursor object we will be able to execute our commands.
'''

cur.execute('SELECT * FROM notes')
one = cur.fetchone()
all = cur.fetchall()
'''
To execute commands on the Postgres database, you call the execute method on the Cursor object with a stringified SQL command.
the cur object calls the execute method and, if it is successful, will return None.
To get the returned value (or values) from your query, you need to call one of the two methods: fetchone() or fetchall().
The fetchone() method returns the first row result or None and
the fetchall() method returns a list of each row in the table or an empty list [] if there are no rows.
'''
