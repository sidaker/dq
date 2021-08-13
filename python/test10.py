import sys
import os
import glob
import re
import json
import datetime
import time
import shutil
import zipfile
import urllib.parse
import urllib.request
import logging
import csv
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

#adt = "2021-07-14 17:10:00"
#adt = "04:20:00"
#adt = "7/15/2021 12:00:00"

#adt = "12/07/2021 15:50:00"
adt = "02/07/2021 13:50:00"
adt = None
#datetime.datetime.strptime(adt[:10], '%Y-%m-%d')
try:
    #adt = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalDateTime')
    time.strptime(adt[11:], '%H:%M:%S')
    time.strptime(adt[:10], '%Y-%m-%d')
    print("Inside try %s", adt)
except ValueError:
    print('Invalid Arrival date - flightdetails_arrivaldatetime: %s', adt)
    try:
        print(datetime.datetime.strptime(adt[:10], '%Y-%m-%d'))
    except Exception:
        print("grace")
except TypeError:
    print("1900")
