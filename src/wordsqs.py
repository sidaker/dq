from collections import defaultdict
# get count of words per line.

def get_wordsperline(filename):
    print("Reading file", filename)
    with open(filename,'rt') as f:
        for lineno,line in enumerate(f,1):
            fields = line.split()
            print("line no: " , lineno , "words", len(fields))

# get in which line a word occurs and build a dictionary with it.
# word hello occurs in lines 1,9. city occurs in line 3.
# A defaultdict will never raise a KeyError
#
def build_dict_lineno_of_words(filename):
    word_list = defaultdict(list)

    with open(filename,'r') as f:
        lines = f.readlines()

    for idx,line in enumerate(lines,1):
        words = [w.strip().lower() for w in line.split()]
        for word in words:
            word_list[word].append(idx)

    return word_list


get_wordsperline("Notes")
a=build_dict_lineno_of_words("Notes")
print(a)
# check where the word python appears
print(a['python'])
# Can help answer lot of questions like which word appeared most, appeared least, total number of words in the list.
