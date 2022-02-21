import csv
from faker import Faker
import datetime
import os

from faker.providers import BaseProvider

# create new provider class
class MyNationality(BaseProvider):
    ctries=["GBR", "IND", "USA", "TLS", "CAN"]
    def foo(self) -> str:
        return 'bar'

def datagenerate(records, headers):
    fake = Faker('en_GB')
    fake1 = Faker('en_GB')   # To generate phone numbers
    filename = '/Users/sbommireddy/Documents/python/assignments/dq/faker_testdata/' + 'bitd_BXBITDExtract_20201224T040956.csv'
    with open(filename, 'wt') as csvFile:
        fake.add_provider(MyNationality)
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for i in range(records):
            full_name = fake.name()
            FLname = full_name.split(" ")
            Fname = FLname[0]
            Lname = FLname[1]
            ctr = fake.random_element(elements=('GBR', 'IND', 'BAN', 'USA'))

            writer.writerow({
                    "Record ID" : fake.random_number(digits=7),
                    "Forename" : Fname,
                    "Surname": Lname,
                    "Date of Birth" : fake.date(pattern="%d/%m/%Y", end_datetime=datetime.date(2000, 1,1)),
                    "Nationality" : ctr,
                    "Document Type": 'P',
                    "Issuing State" : ctr,
                    "Document Number" : fake.bothify(text='???######', letters='ABCDE'),
                    "Sex" : fake.random_element(elements=('M', 'F')),
                    "Expiration Date" : fake.date(pattern="%d/%m/%Y", end_datetime=datetime.date(2030, 1,1)),
                    "Date Acquired" : fake.date_time_this_year(),
                    "Travel Direction":'arrivals',
                    "LocationID": 'EDX',
                    "DeviceID": fake.bothify(text='EDX???###', letters='ABCDFGH'),
                    "Platform Type": 'F',
                    })

if __name__ == '__main__':
    records = 20000
    headers = ["Record ID", "Forename", "Surname", "Date of Birth", "Nationality", "Document Type",
               "Issuing State", "Document Number", "Sex","Expiration Date", "Date Acquired", "Travel Direction", "LocationID", "DeviceID", "Platform Type"]
    datagenerate(records, headers)
    print(os.path.dirname(os.path.realpath(__file__)))
    print("CSV generation complete!")
