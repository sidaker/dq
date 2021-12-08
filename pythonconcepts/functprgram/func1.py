def sort_by_last_letter(strings):
    # last_letter is a local function
    def last_letter(s):
        return s[-1]
    # print(last_letter)
    # new function is created evrry timke def is executed
    return sorted(strings,key=last_letter)

aa = sort_by_last_letter(["Advik", "Loikhi", "Daddy", "Amma"])
print(aa)


def encl():
    x = 'closed over'
    def lofunc():
        print(x)
    return lofunc

bb = encl()
print(bb.__closure__)
