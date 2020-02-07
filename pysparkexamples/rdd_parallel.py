#reduceByKey() with custom parallelism in Python
data = [("a", 3), ("b", 4), ("a", 1)]

#sc.parallelize(data).reduceByKey(lambda x, y: x + y) # Default parallelism
rdd4 = sc.parallelize(data).reduceByKey(lambda x, y: x + y, 4) # Custom parallelism

'''
Sometimes, we want to change the partitioning of an RDD outside the context of
 grouping and aggregation operations.
 For those cases, Spark provides the repartition() function, which shuffles
 the data across the network to create a new set of partitions.
 Keep in mind that repartitioning your data is a fairly expensive operation.
 Spark also has an optimized version of repartition() called coalesce() that
 allows avoiding data movement, but only if you are decreasing the number of
 RDD partitions. To know whether you can safely call coalesce(),
 you can check the size of the RDD using rdd.getNumPartitions() in Python
'''

'''
Partitioning will not be helpful in all applications—for example,
if a given RDD is scanned only once, there is no point in partitioning it in
advance. It is useful only when a dataset is reused multiple times in
key-oriented operations such as joins.
'''

'''
Spark’s partitioning is available on all RDDs of key/value pairs, and causes
the system to group elements based on a function of each key.
Although Spark does not give explicit control of which worker node each key
goes to (partly because the system is designed to work even if specific nodes
fail), it lets the program ensure that a set of keys will appear together on
some node. For example, you might choose to hash- partition an RDD into 100
partitions so that keys that have the same hash value modulo 100 appear on
the same node. Or you might range-partition the RDD into sorted ranges of keys
so that elements with keys in the same range appear on the same node.
'''


'''
sortByKey() and groupByKey() will result in range-partitioned and hash-partitioned RDDs,
respectively. On the other hand, operations like map() cause the new RDD to
forget the parent’s partitioning information, because such operations could
theoretically modify the key of each record.
he operations that benefit from partitioning are
cogroup(), groupWith(), join(), leftOuterJoin(), rightOuter Join(),
groupByKey(), reduceByKey(), combineByKey(), and lookup()
'''

'''
For operations that act on a single RDD, such as reduceByKey(), running on a pre- partitioned RDD will cause all the values for each key to be computed locally on a single machine, requiring only the final, locally reduced value to be sent from each worker node back to the master. For binary operations, such as cogroup() and join(), pre-partitioning will cause at least one of the RDDs (the one with the known partitioner) to not be shuffled. If both RDDs have the same partitioner, and if they are cached on the same machines (e.g., one was created using mapValues() on the other, which preserves keys and partitioning) or if one of them has not yet been com‐ puted, then no shuffling across the network will occur.
'''

'''
The flipside, however, is that for transformations that cannot be guaranteed to pro‐ duce a known partitioning, the output RDD will not have a partitioner set. For example, if you call map() on a hash-partitioned RDD of key/value pairs, the function passed to map() can in theory change the key of each element, so the result will not have a partitioner.
'''

'''
Spark does not analyze your functions to check whether they retain the key. Instead, it provides two other operations, mapValues() and flatMap Values(), which guarantee that each tuple’s key remains the same.
'''

'''
All that said, here are all the operations that result in a partitioner being set on the output RDD: cogroup(), groupWith(), join(), leftOuterJoin(), rightOuter Join(), groupByKey(), reduceByKey(), combineByKey(), partitionBy(), sort(), mapValues() (if the parent RDD has a partitioner), flatMapValues() (if parent has a partitioner), and filter() (if parent has a partitioner). All other operations will produce a result with no partitioner.
'''
