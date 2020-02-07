
'''
When we ask Spark to persist an RDD, the nodes that compute the RDD store their
partitions.
In Python, we always serialize the data that persist stores,
so the default is instead stored in the JVM heap as pickled objects.
When we write data out to disk or off-heap storage, that data is also always
serialized.
if desired we can replicate the data on two machines by adding _2 to the end of
 the storage level

If a node that has data persisted on it fails, Spark will recompute the lost
partitions of the data when needed. We can also replicate our data on multiple
nodes if we want to be able to handle node failure without slowdown.
'''

'''
partitioning lets users control the layout of pair RDDs across nodes.
Using controllable partitioning, applications can some‐ times greatly reduce
 communication costs by ensuring that data will be accessed together and
 will be on the same node. This can provide significant speedups.
 Choosing the right partitioning for a distributed dataset is similar to
 choosing the right data struc‐ ture for a local one—in both cases,
 data layout can greatly affect performance.
'''
