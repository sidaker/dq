
def main():

    lis1 = ['Sun','Mon','Tue','Wed']
    lis2 = ['Dim','Lun','Mar','Mer']

    i = iter(lis1)
    print(next(i))
    print(next(i))

    with open("python/Notes.txt","r") as fp:
        # pass sentinel value '' to the iter
        # iterator stops processing when it encounters '' empty string.
        for line in iter(fp.readline,''):
            print(line)

    for i,m in enumerate(lis1,start=1):
        print(i,m)

    # Use zip to combine sequences
    for m in zip(lis1,lis2):
        print(m)

        
if __name__ == '__main__':
    main()
