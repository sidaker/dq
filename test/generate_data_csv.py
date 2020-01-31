import csv
import random
from time import time
from decimal import Decimal
from faker import Faker

#RECORD_COUNT = 100000
RECORD_COUNT = 1000
fake = Faker()

def create_csv_file():
    with open('./bitd_1k.csv', 'w', newline='') as csvfile:
        fieldnames = ['Record ID', 'Forename', 'Surname', 'Date of Birth', 'Nationality',
                      'Document Type','Issuing State','Document Number', 'Date Acquired', 'Travel Direction',
                      'LocationID', 'DeviceID',
                      'Platform Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(RECORD_COUNT):
            writer.writerow(
                {
                    'Record ID': fake.name(),
                    'Forename': fake.name(),
                    'Surname': fake.email(),
                    'Date of Birth': fake.random_int(min=100, max=199),
                    'Nationality': fake.random_int(min=1, max=9),
                    'Document Type': float(Decimal(random.randrange(500, 10000))/100),
                    'Issuing State': fake.sentence(),
                    'Document Number': fake.street_address(),
                    'Date Acquired': fake.city(),
                    'Travel Direction': fake.state(),
                    'LocationID': fake.country(),
                    'DeviceID' : fake.random_int(min=1, max=9),
                    'Platform Type' : fake.random_int(min=1, max=9)

                }
            )

if __name__ == '__main__':
    start = time()
    create_csv_file()
    elapsed = time() - start
    print('created csv file time: {}'.format(elapsed))
