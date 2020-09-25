from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
import calendar

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
