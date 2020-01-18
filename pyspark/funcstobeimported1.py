def scopeTest(number):
    try:
        number += 1
        return number
    except Exception as e:
        print(e)
