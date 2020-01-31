import csv
import random
from time import time
from decimal import Decimal
from faker import Faker
import datetime

# http://zetcode.com/python/faker/
RECORD_COUNT = 3000000
#RECORD_COUNT = 1000
fake = Faker('en_GB')
words = ['forest', 'blue', 'cloud', 'sky', 'wood', 'falcon']
docttype = ['CR', 'V<', 'P<', 'VI', 'ID', 'VR','VS','IR','VA']

def create_csv_file():
    with open('./bitd_3000k.csv', 'w', newline='') as csvfile:
        fieldnames = ['Record ID', 'Forename', 'Surname', 'Date of Birth', 'Nationality',
                      'Document Type','Issuing State','Document Number', 'Date Acquired', 'Travel Direction',
                      'LocationID', 'DeviceID',
                      'Platform Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(RECORD_COUNT):
            writer.writerow(
                {
                    'Record ID': fake.random_int(1, 999999),
                    'Forename': fake.first_name(),
                    'Surname': fake.last_name(),
                    'Date of Birth': fake.date_of_birth(), # YYYY-MM-DD by default
                    'Nationality': fake.country()[:3].upper(),
                    'Document Type': fake.text()[:3].upper(), # fake.text()
                    'Issuing State': fake.country()[:3].upper(),
                    'Document Number': fake.random_int(100000, 900000),
                    'Date Acquired': fake.date_time_this_month(),
                    'Travel Direction': 'arrivals',
                    'LocationID': fake.country()[:3].upper(),
                    'DeviceID' : 'LUNABC1',
                    'Platform Type' : 'C'

                }
            )

if __name__ == '__main__':
    start = time()
    create_csv_file()
    elapsed = time() - start
    print('created csv file time: {}'.format(elapsed))
