import re
import os
import sys
import time
import random
import datetime
from dateutil.relativedelta import relativedelta

PATTERN = re.compile("20[0-9]{2}-[0-9]{1,2}-[0-9]{1,2}")
TWOMONTHSPLUSCURRENT = ((datetime.date.today() - relativedelta(months=2)).replace(day=1) - datetime.timedelta(days=1))
THIRTYDAYS = (datetime.date.today() - datetime.timedelta(days=30))
TODAY = datetime.date.today()

# CASE1 : Filter a list of dictionaries
l = [{'key':10}, {'key':4}, {'key':8}]

def condition(dic):
    ''' Define your own condition here'''
    return dic['key'] > 7

filtered = [d for d in l if condition(d)]

print(filtered)
# [{'key': 10}, {'key': 8}]

# CASE2 : Filter a list of dictionaries
l2 = [{'Values': ['2020-08-01/180019']}, {'Values': ['2020-09-01/180019']}, {'Values': ['2020-10-01/180019']}]
def condition(dic):
    ''' Define your own condition here'''
    match = PATTERN.search(dic['Values'][0]).group(0)
    #print(match)
    return dic['Values'][0] < str(THIRTYDAYS)

filtered2 = [d for d in l2 if condition(d)]
#print(filtered2)

# CASE3 : Filter a list of dictionaries
l2 = [{'Values': ['2020-08-01/180019'], 'StorageDescriptor': {'Columns':'hello'}}, {'Values': ['2020-09-01/180019'], 'StorageDescriptor': {'Columns':'world'}}, {'Values': ['2020-10-01/180019'], 'StorageDescriptor': {'Columns':'lucky'}}]
def condition(dic,retention):
    ''' Define your own condition here'''
    match = PATTERN.search(dic['Values'][0]).group(0)
    print(match)
    return dic['Values'][0] < str(retention)

filtered2 = [d for d in l2 if condition(d,THIRTYDAYS)]
print(filtered2)
