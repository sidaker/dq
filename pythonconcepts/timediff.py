from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
import time


#st_dttime =  datetime.date(datetime.now())
st_dttime =  datetime.now()
time.sleep(62)
#curr_dttime =  datetime.date(datetime.now())
curr_dttime = datetime.now()
print(curr_dttime)
print(curr_dttime - st_dttime )


#first_time = datetime.datetime.now()
#later_time = datetime.datetime.now()
difference = curr_dttime - st_dttime
seconds_in_day = 24 * 60 * 60
timedelta(0, 8, 562000)
a =divmod(difference.days * seconds_in_day + difference.seconds, 60)
print(a)
