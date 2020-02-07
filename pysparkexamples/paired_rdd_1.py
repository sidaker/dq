from pyspark.sql import SparkSession
from functools import reduce

listoftups = [(1, 2), (3, 4), (3, 6), (2,5), (4,7) , (1,6)]
listoftups2 = [ (3, 9), (3, 12),  (4,8)]
spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()

pairRDD1 = spark.sparkContext.parallelize(listoftups,2)
pairRDD2 = spark.sparkContext.parallelize(listoftups2,2)
pairRDD1.persist()

'''
reduceByKey() runs several parallel reduce operations, one for each key in the
dataset, where each operation combines values that have the same key.
Because datasets can have very large numbers of keys, reduceByKey() is not
implemented as an action that returns a value to the user program.
Instead, it returns a new RDD consisting of each key and the reduced value
for that key.
reduceByKey() and foldByKey() will automatically perform combining locally on
each machine before computing global totals for each key.
The user does not need to specify a combiner.
The more general combineByKey() interface allows you to customize combining
behavior.
'''
print("*"*50)
print("Reduce by Key - Combine values with the same key.")
print(pairRDD1.reduceByKey(lambda x,y: x+y).collect())

print("*"*50)
print("Group by Key - Groups values with the same key.")
print(pairRDD1.groupByKey().collect())
print(list((j[0],j[1])) for j in pairRDD1.groupByKey().collect())
# You can use groupByKey with map to get counts per key though you always perfer redyceByKey over groupByKey
'''
All executors when using groupByKey must keep all values for a given key
in memory before applying the function to them.
When there is masive key skew, this can cause memory issues as some partitions
may be overloaded with tons of values for a given key.
'''

def addFunc(left,right):
    return left + right
print(pairRDD1.groupByKey().map(lambda x:(x[0],reduce(addFunc, x[1]))).collect())

print("*"*50)
print("Act Only on the values using mapValues")
print(pairRDD1.mapValues(lambda x:x+1).collect())

print("*"*50)
print("using flatMapValues")
print(pairRDD1.flatMapValues(lambda x:range(x,6)).collect())

print("*"*50)
print("Print only values")
print(pairRDD1.values().collect())

print("*"*50)
print("Print only keys")
print(pairRDD1.keys().collect())

print("*"*50)
print("sortByKey ")
print(pairRDD1.sortByKey().collect())

print("*"*50)
print("subtractByKey ")
print(pairRDD1.subtractByKey(pairRDD2).collect())

print("*"*50)
print("join ")
print(pairRDD1.join(pairRDD2).collect())

print("*"*50)
print("left outer join ")
print(pairRDD1.leftOuterJoin(pairRDD2).collect())

# filter on 2nd element of paired RDD.
print("*"*50)
print("filter on 2nd element and print only values>5 ")
print(pairRDD1.filter(lambda keyValue: keyValue[1] > 5).collect())

#Per-key average with reduceByKey() and mapValues() in Python
print("*"*50)
print("Per Key Average ")
print(pairRDD1.mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1])).collect())
