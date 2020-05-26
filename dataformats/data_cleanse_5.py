import pandas as pd
import datetime
from dateutil.parser import parse
import time

# "DateAcquired": "2020-04-30 04:29:58"
# "ExpirationDate": null,
# "DateofBirth": "25/06/1989"
#  DateAcquired
# "DateAcquired": "2020-04-30 05:01:14"

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def monthcheck(month):
       return 0 < month <= 12


def daycheck(month,day,year):
    monthlist1 = ["01","03","05","07","08","10","12"] ## monthlist for months with 31 days.
    monthlist2 = ["04","06","09","11"] ## monthlist for months with 30 days.

    if(month in monthlist1):
        return 0 < day <= 31

    elif(month in monthlist2):
        return 0 < day <= 30

    else:
        if isleapyear(year): ## if the parameter day is between 1 and 28,return True.
            return 1 <= day <= 29
        else:
            return 1 <= day <= 28


def isleapyear(year):
    if (year % 4) == 0:
       if (year % 100) == 0:
           if (year % 400) == 0:
               return True
           else:
               return False
       else:
           return True
    else:
       return False

def yearcheck(year):
    if len(year) >= 1 and len(year) <= 4: ## Check if year has between 1 to 4 numbers and return True.
        return True
    else:
        return False


def datevalidator2(date):
    #date = str(input("Enter the date in dd/mm/yyyy format: ")) ## Input date in the given format.
    # Check if 10 characters
    # date is of type series.

    if(date is None):
        return "01/01/1900"

    if(len(date)!=10):
        print("The date {0} is invalid and not 10 characters long.".format(date))
        return "01/01/1900"

    if(is_date(date)):
        pass
    else:
        return "01/01/1900"

    try:
         datetime.datetime.strptime(date, '%d/%m/%Y')
    except:
         print('Invalid date. Not Parsed {0}'.format(date))
         return "01/01/1900"

    #  Check if input date contains only digits and separated by /

    day,month,year = date.split("/") ## split the date into 3 separate variables.

    if(month.isdigit() and day.isdigit() and year.isdigit()):
        pass
    else:
        return "01/01/1900"

    monthvalidity = monthcheck(int(month))
    dayvalidity = daycheck(month,int(day),int(year))
    yearvalidity = yearcheck(year)

    if monthvalidity and dayvalidity and yearvalidity: ## check if all 3 variables are valid or True
        return date
    else:
        return "01/01/1900"

path = "/Users/sbommireddy/Downloads/part-00000-6b87b6b6-551a-436d-a256-23c60f2b3cd7-c000.snappy.parquet"
#path = "/Users/sbommireddy/Documents/python/assignments/dq/dataformats/part-00000-be346b50-e18c-407c-bff5-b7cebc49d43a-c000.snappy.parquet"
ant = pd.read_parquet(path, engine='pyarrow', columns=None)
print("---------------------------")
ant1 = ant.drop(['header','Minute'],axis=1)
print(ant1['body'].head())
print("---------------------------")
#df3 = pd.DataFrame([x for x in df['dic']])
#feature3 = [d.get('Feature3') for d in df.dic]
print("#####*****************************")
# Use apply on ant1 and extract each value
#ant1
print(ant1['body'].apply(pd.Series).head())
print("######*****************************")
list1 = []
for label, content in ant1.items():
    for i in content:
        list1.append(i)

df3 =  pd.DataFrame.from_records(list1)
print("--------")
df3.loc[:, 'DateofBirth'] = df3.loc[:, 'DateofBirth'].apply(lambda x: datevalidator2(x))
#df3.loc[:, 'ExpirationDate'] = df3.loc[:, 'ExpirationDate'].apply(lambda x: datevalidator2(x))
#df3.loc[:, ['DateofBirth','ExpirationDate']] = df3.loc[:, ['DateofBirth','ExpirationDate']].apply(lambda x: datevalidator2(x))
df3['PartDateAcquired'] = df3.loc[:, 'DateAcquired'].apply(lambda x: datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S').date())
df3.to_parquet("/Users/sbommireddy/Documents/python/assignments/dq/dataformats/files/xx.snappy.parquet", engine='pyarrow', compression='snappy', partition_cols = ['PartDateAcquired'])

df3.info()
df3.count()
print(df3['DateofBirth'].head())
print("Done")
print("--------")
