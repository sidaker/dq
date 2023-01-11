def find_match(message):
    match message:
        case ['BEEP', freq, times]:
            print("BEEP")
        case 'love':
            print("Got love")
        case _:
            print("Mind the case-default")    

find_match(['BEEP',1,3])
find_match(['bEEP',1,3])
find_match('love')
