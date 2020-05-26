import datetime

string = "19 Nov 2015  18:45:00.000"
date = datetime.datetime.strptime(string, "%d %b %Y  %H:%M:%S.%f")

print(date)
