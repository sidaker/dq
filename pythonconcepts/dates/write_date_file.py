import csv
import time
from datetime import datetime, timedelta

with open("/tmp/highwatermark.csv", "w") as f:
    f.write((datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d'))
