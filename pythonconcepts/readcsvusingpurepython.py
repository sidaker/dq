with open("../data/population_data.csv") as f:
    lis = [line.split() for line in f]        # create a list of lists
    for i, x in enumerate(lis):              #print the list items
        print("line{0} = {1}".format(i, x))
        if i >10:
            break


def print_lines(n, file_name):
    f = open(file_name)
    for i in range(n):
        print(f.readline())
    f.close()

print_lines(1, 'population_data.json')
