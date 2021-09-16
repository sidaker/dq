import psycopg2
import csv
import sys


filed = '/Users/sbommireddy/Desktop/code/FLIGHTSTATS_20201106.csv'
filec = '/Users/sbommireddy/Desktop/code/FLIGHTSTATS_20201106_new.csv'


reader = csv.reader(open(filed, "r"), skipinitialspace=True)
writer = csv.writer(open(filec, 'w'),quoting=csv.QUOTE_NONE)

for row in reader:
    writer.writerow(row)

conn = psycopg2.connect("dbname=learning user=sid")
cur = conn.cursor()

# The Postgres command to load files directy into tables is called COPY. It takes in a file (like a CSV) and automatically loads the file into a Postgres table.
# The method to load a file into a table is called copy_from. Like the execute() method, it is attached to the Cursor object.
# The copy_from arguments requires a file to load (without the header), the tablename it should load into, as well as a delimiter (the key argument sep).


with open(filec, 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    # load csv file into users table.
    try:
        cur.copy_from(f, 'stg_flightstats', sep=',', null='')
        cur.copy_expert("COPY stg_flightstats TO STDOUT WITH CSV HEADER", sys.stdout)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)


'''
Above is not the most efficient way of doing it.
As you can see, we had to loop through every single row from the file just to insert them into the database
'''


conn.close()
