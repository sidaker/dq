from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)

'''
rdd1 = spark.sparkContext.parallelize([1, 2, 3, 4])
rdd1.map(lambda x:x * x).collect()
[1, 4, 9, 16]
rdd1.filter(lambda x:x > 1).collect()
[2, 3, 4]

rdd2 = spark.sparkContext.parallelize([1, 2, 3, 3])
rdd2.distinct().collect()
[1, 2, 3]


[1, 2, 3, 4, 1, 2, 3, 3]
rdd1.intersection(rdd2).collect()
[1, 2, 3]

rdd1.subtract(rdd2).collect()
[4]

rdd1.cartesian(rdd2).collect()
[(1, 1), (1, 2), (1, 3), (1, 3), (2, 1), (2, 2), (2, 3), (2, 3), (3, 1), (3, 2), (3, 3), (3, 3), (4, 1), (4, 2), (4, 3), (4, 3)]

rdd1.collect()
[1, 2, 3, 4]

rdd1.flatMap(lambda x: range(1,x)).collect()
[1, 1, 2, 1, 2, 3]

sc.parallelize([3,4,5]).flatMap(lambda x: range(1,x)).collect()
[1, 2, 1, 2, 3, 1, 2, 3, 4]

As you see
range(1,3) is 1,2.
range(1,4) is 1,2,3 and so on and so forth.
map would return range object where as flatMap would flatten the range object.

rdd1.map(lambda x: range(1,x)).collect()
[range(1, 1), range(1, 2), range(1, 3), range(1, 4)]

spark.sparkContext.parallelize([3,4,5]).reduce(lambda x,y: x+y)
12

Similar to reduce() is fold(), which also takes a function with the same signature as
needed for reduce(), but in addition takes a “zero value” to be used for the initial call
on each partition. The zero value you provide should be the identity element for your
operation; that is, applying it multiple times with your function should not change
the value (e.g., 0 for +, 1 for *, or an empty list for concatenation).

spark.sparkContext.parallelize([3,4,5]).reduce(lambda x,y: x+y)
12
spark.sparkContext.parallelize([3,4,5]).collect()
[3, 4, 5]
spark.sparkContext.parallelize([3,4,5]).count()
3
spark.sparkContext.parallelize([3,4,5]).countByValue()
defaultdict(<class 'int'>, {3: 1, 4: 1, 5: 1})

spark.sparkContext.parallelize([3,4,5]).take(2)
[3, 4]

spark.sparkContext.parallelize([3,4,5]).top(2)
[5, 4]

'''

inputRDD = sc.textFile("log.txt",8)
errorsRDD = inputRDD.filter(lambda x: "ERROR" in x)
warningsRDD = inputRDD.filter(lambda x: "WARN" in x)
badLinesRDD = errorsRDD.union(warningsRDD)

print("*"*50)
print("Input had " + str(badLinesRDD.count()) + " concerning lines")
print("*"*50)
print ("Here are 10 examples:")
for line in badLinesRDD.take(10):
    print(line)

print("*"*50)

"""
If you would like to reuse an RDD in multiple actions, you can ask Spark to
persist it using RDD.persist().
"""

"""
Actions are operations that return a result to the driver pro‐
gram or write it to storage, and kick off a computation.
"""


"""
 transformations return RDDs, whereas actions return some other data type.
"""

'''
Spark keeps
track of the set of dependencies between different RDDs, called the lineage graph. It
uses this information to compute each RDD on demand and to recover lost data if
part of a persistent RDD is lost.
'''

'''
RDDs also have a collect() function to retrieve the entire RDD.
Keep in mind that your entire dataset must fit in memory on a
single machine to use collect() on it, so collect() shouldn’t be used on large
datasets.
Use take() to retrieve a small number of elements in the RDD
at the driver program.
'''

'''
It is important to note that each time we call a new action, the entire RDD must be
computed “from scratch.” To avoid this inefficiency, users can persist intermediate
results
'''

'''
Spark uses lazy evaluation to reduce the number of passes it has to take over our data
by grouping operations together. In systems like Hadoop MapReduce, developers
often have to spend a lot of time considering how to group together operations to
minimize the number of MapReduce passes. In Spark, there is no substantial benefit
to writing a single complex map instead of chaining together many simple opera‐
tions. Thus, users are free to organize their program into smaller, more manageable
operations.
'''


'''
One issue to watch out for when passing functions is inadvertently serializing the
object containing the function. When you pass a function that is the member of an
object, or contains references to fields in an object (e.g., self.field), Spark sends the
entire object to worker nodes, which can be much larger than the bit of information
you need. Sometimes this can also cause your program to fail, if
your class contains objects that Python can’t figure out how to pickle.

def getMatchesFunctionReference(self, rdd):
 # Problem: references all of "self" in "self.isMatch"
 return rdd.filter(self.isMatch)
 def getMatchesMemberReference(self, rdd):
 # Problem: references all of "self" in "self.query"
 return rdd.filter(lambda x: self.query in x)

def getMatchesNoReference(self, rdd):
 # Safe: extract only the field we need into a local variable
 query = self.query
 return rdd.filter(lambda x: query in x)

'''


'''
Note that distinct() is expensive, however, as it requires shuffling all the data over
the network to ensure that we receive only one copy of each element.
'''

'''
While intersection() and union() are two sim‐
ilar concepts, the performance of intersection() is much worse since it requires a
shuffle over the network to identify common elements.
'''
