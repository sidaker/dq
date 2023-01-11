from collections import Counter
words = [
       'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
       'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
       'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
       'my', 'eyes', "you're", 'under'
]

wc = Counter(words)
print(type(wc))
print(wc['look'])
print(wc)


morewords = ['why','are','you','not','looking','in','my','eyes']
wc.update(morewords)
print(wc)
print(wc.most_common(3))
