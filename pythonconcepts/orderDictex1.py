from collections import OrderedDict

def main():
    # team and win and loss
    sportsTeam = [("Royals", (18,12)), ("Rockets", (24,6)),
                ("C", (20,10)), ("D", (22,9)),
                ("Kings", (15,15)), ("Chargers", (20,9)),
                ("Jets", (18,12)), ("Warriros", (25,5))]
    # sort by wins asc 15,18,18,20 etc.
    sortedteams1 = sorted(sportsTeam, key = lambda t:t[1][0])
    sortedteams = sorted(sportsTeam, key = lambda t:t[1][0],reverse=True)
    print(sortedteams)

    teams = OrderedDict(sortedteams)
    print(teams)
    tm, wl = teams.popitem(False)
    print(tm,wl)
    print(teams)
    tm, wl = teams.popitem(True)
    print(teams)





if __name__ == '__main__':
    main()
