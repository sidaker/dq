words = [
       'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
       'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
       'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
       'my', 'eyes', "you're", 'under'
]


from collections import Counter
word_cts = Counter(words)
print(word_cts)
print(word_cts['eyes'])
print(word_cts.most_common(3))

morewords = ['why','are','you','not','looking','in','my','eyes']
word_cts.update(morewords)
print(word_cts['eyes'])


a = Counter(words)
b = Counter(morewords)
print(a)
print(b)
c = a + b
print(c)
