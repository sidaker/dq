from random import randrange

def main():
    num = randrange(100)
    print(num)
    while True:
        #inside loop
        try:
            print("okay")
            guess = int(input("enter number?"))
            print(f'you entered {guess}')
        #except:
        #Above  will catch all exceptions including System exceptions like Keyboard interrupt.
        except ValueError:
            print("enter a proper integer")
            continue

        if guess == num:
            print("You won the lotto!!")
            break


if __name__ == '__main__':
    main()
    print("End of program")
