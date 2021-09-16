def main():

    ctemps = [0,12,20,34,100]
    ftemps = [32,54,64,72,80,85]

    print(list(map(lambda t: (t-32) * 5/9, ftemps)))
    print(list(map(lambda t: (t*9/5) + 32, ctemps)))


if __name__ == '__main__':
    main()
