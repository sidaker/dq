import datetime

string = "19 Nov 2015  18:45:00.000"
date = datetime.datetime.strptime(string, "%d %b %Y  %H:%M:%S.%f")

print(date)



print(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
