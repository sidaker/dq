from pyspark.sql import SparkSession

# https://github.com/databricks/learning-spark/blob/master/src/python/PerKeyAvg.py
spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()
def perKeyAvg(nums):
    """Compute the avg"""
    sumCount = nums.combineByKey((lambda x: (x, 1)),
                                 (lambda x, y: (x[0] + y, x[1] + 1)),
                                 (lambda x, y: (x[0] + y[0], x[1] + y[1])))
    return sumCount.collectAsMap()

input = [("coffee", 1), ("pandas", 2), ("coffee", 3), ("very", 4)]
nums = spark.sparkContext.parallelize(input)

avg = perKeyAvg(nums)
print(avg)

'''
combineByKey() is the most general of the per-key aggregation functions.
Most of the other per-key combiners are implemented using it.
Like aggregate(), combineBy Key() allows the user to return values that are
not the same type as our input data.
To understand combineByKey(), it’s useful to think of how it handles each
element it processes. As combineByKey() goes through the elements in a
partition, each element either has a key it hasn’t seen before or has the same
key as a previous element.
If it’s a new element, combineByKey() uses a function we provide, called
create Combiner(), to create the initial value for the accumulator on that key.
Note that this happens the first time a key is found in each partition,
rather than only the first time the key is found in the RDD.
If it is a value we have seen before while processing that partition, it will
instead use the provided function, mergeValue(), with the current value for the
 accumulator for that key and the new value.
Since each partition is processed independently, we can have
multiple accumulators for the same key. When we are merging the results from
 each partition, if two or more partitions have an accumulator for the same key
  we merge the accumulators using the user-supplied mergeCombiners() function.
'''
