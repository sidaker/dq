from pyspark import SparkContext
# spark-submit --executor-memory 3G --total-executor-cores 2 broadcast_example.py
sc = SparkContext("local", "Broadcast app")
words_new = sc.broadcast(["Sid", "Likhi", "Advik", "Bargu", "Sammu"])
# In this case, words_new is a broadcast variable available for all tasks across all nodes.
'''
Broadcast variables allow the programmer to keep a read-only variable cached on each
machine rather than shipping a copy of it with tasks.
They can be used, for example, to give every node a copy of a large input dataset
 in an efficient manner. Spark also attempts to distribute broadcast variables using
 efficient broadcast algorithms to reduce communication cost.
'''
data = words_new.value
print("Stored data -> {}".format(data))
elem = words_new.value[2]
