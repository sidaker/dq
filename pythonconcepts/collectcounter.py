from collections import Counter


def main():
    count1()

def count1():
    class1 = ["A","B","C","D","E","F","A","B","C",'A']
    class2 = ["G","H","I","J","K","L","A","B","A","B"]

    c1 = Counter(class1)
    c2 = Counter(class2)

    print(c1["A"])
    print(c1.values())
    print(sum(c1.values()))

    # combine the two classes
    c1.update(class2)
    print("*"*50)
    print(c1["A"])
    print(c1.values())
    print(c1.keys())
    print(sum(c1.values()))
    print(c1.most_common(3))
    print("*"*50)
    c1.subtract(class2)
    print(c1["A"])

    print(c1 & c2)




if __name__ == '__main__':
    main()
