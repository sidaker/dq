from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
import calendar

def months_between(start_date, end_date):
    """
    Given two instances of ``datetime.date``, generate a list of dates on
    the 1st of every month between the two dates (inclusive).

    e.g. "5 Jan 2020" to "17 May 2020" would generate:

        1 Jan 2020, 1 Feb 2020, 1 Mar 2020, 1 Apr 2020, 1 May 2020

    """
    if start_date > end_date:
        raise ValueError(f"Start date {start_date} is not before end date {end_date}")

    year = start_date.year
    month = start_date.month

    while (year, month) <= (end_date.year, end_date.month):
        yield date(year, month, 1)

        # Move to the next month.  If we're at the end of the year, wrap around
        # to the start of the next.
        #
        # Example: Nov 2017
        #       -> Dec 2017 (month += 1)
        #       -> Jan 2018 (end of year, month = 1, year += 1)
        #
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

def main():
    #Today
    print(date.today())
    print(datetime.date(datetime.now()))
    print(date.today().day)
    print(date.today().year)
    print(date.today().month)
    # Print week day numbers
    print(date.today().weekday())
    weeklist = ["mon","tue","wed","thu","fri","sat","sund"]
    print(weeklist[date.today().weekday()])

    print("*"*50)
    print(datetime.now())
    print(datetime.now().ctime())
    print(datetime.now().astimezone())
    print(datetime.now().date())
    print(datetime.now().time())
    print(datetime.now().timestamp())
    print(datetime.now().day)

    # on datetime object you have method strf to manipulate
    print("*"*50)
    print(datetime.now().strftime("%Y-%m-%d"))
    print(datetime.now().strftime("%y-%B-%d"))
    print(datetime.now().strftime("%Y-%b-%d"))
    print(datetime.now().strftime("%a %b %x %X"))
    print(datetime.now().strftime("%c Locale date and time"))
    print(datetime.now().strftime("%I %H %M %S %p"))

    # timedelta
    print(timedelta(days=365,weeks =3 ,hours=5,minutes=1))
    print(datetime.now() + timedelta(days=365,hours=5,minutes=1))
    print((datetime.now() + timedelta(days=365,hours=5)).strftime("%Y-%m-%d %H:%M:%S"))

    # Days till 1st April.
    today = date.today()
    afd = date(today.year,4,1)
    print(afd,today)
    if(today<afd):
        print(afd-today)
    else:
        afd = afd.replace(year = today.year+1)
        print("next year")
        print(afd)
        print(afd-today)

    c = calendar.TextCalendar(calendar.SUNDAY)
    #c = calendar.HTMLCalendar(calendar.SUNDAY)
    st = c.formatmonth(2017,3,0,0)
    print(st)
    print("*"*50)
    for i in c.itermonthdays(2020,9):
        print(i)

    for m in range(1,13):
        print(c.formatmonth(2020,m,0,0))


if __name__ == '__main__':
    main()
    print("*"*50)
    print("Get Months between start and end date")
    start_of_2020 = date(2020, 1, 1) # datetime.date
    today = date.today()

    for month in months_between(start_of_2020, today):
        print(month.strftime("%B %Y"))
        # January 2020, February 2020, March 2020, …
