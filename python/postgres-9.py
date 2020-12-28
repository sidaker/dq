import psycopg2
import csv

#reader = csv.reader(open("in.csv", "rb"), skipinitialspace=True)

filed = '/Users/sbommireddy/Desktop/code/FLIGHTSTATS_20201106.csv'
filec = '/Users/sbommireddy/Desktop/code/FLIGHTSTATS_20201106_new.csv'
reader = csv.reader(open(filed, "rb"), skipinitialspace=True)

myFile = open(filec, 'w')

with myFile:
    writer = csv.writer(myFile, quoting=csv.QUOTE_NONE)
    writer.writerows(reader)

'''
python /Users/sbommireddy/Documents/python/assignments/dq/python/postgres-3.py
'''

conn = psycopg2.connect("dbname=learning user=sid")

cur = conn.cursor()

# The Postgres command to load files directy into tables is called COPY. It takes in a file (like a CSV) and automatically loads the file into a Postgres table.
# The method to load a file into a table is called copy_from. Like the execute() method, it is attached to the Cursor object.
# The copy_from arguments requires a file to load (without the header), the tablename it should load into, as well as a delimiter (the key argument sep).


with open(filec, 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    # load csv file into users table.
    cur.copy_from(f, 'stg_flightstats', sep=',')

'''
with open('user_accounts.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row.
    for row in reader:
        cur.execute(
        "INSERT INTO users VALUES (%s, %s, %s, %s)",
        row
    )

'''

'''
Above is not the most efficient way of doing it.
As you can see, we had to loop through every single row from the file just to insert them into the database
'''

conn.commit()
conn.close()
