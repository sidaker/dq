from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import avg

spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()
mylist = [1,2,3,4,10,20,30]
# We can use aggregate() to compute the average of an RDD, avoiding a map() before the fold()
# https://stackoverflow.com/questions/28240706/explain-the-aggregate-functionality-in-spark
numsRDD = spark.sparkContext.parallelize(mylist,2)
sumCount = numsRDD.aggregate(
  (0, 0),
  (lambda local_result, list_element: (local_result[0] + list_element, local_result[1] + 1)),
  (lambda some_local_result, another_local_result: (some_local_result[0] + another_local_result[0], some_local_result[1] + another_local_result[1])))

'''
Actually the zero value should be 'neutral' towards the seqop, meaning it wouldn't interfere with the seqop result,
like 0 towards add, or 1 towards *;
'''
print("*"*50)
print(sumCount[0] / float(sumCount[1]))
print("RDD AverageResult")
print("*"*50)
'''
aggregate() lets you take an RDD and generate a single value that is of a different type than what was stored in the original RDD.

Parameters:

zeroValue: The initialization value, for your result, in the desired format.
seqOp: The operation you want to apply to RDD records. Runs once for every record in a partition.
combOp: Defines how the resulted objects (one for every partition), gets combined.
'''
# cSchema = StructType([StructField("WordList", ArrayType(StringType()))])
# cSchema = StructType([StructField("nums", IntegerType())])
#schema=cSchema
#df = spark.createDataFrame(mylist, IntegerType())
df = spark.createDataFrame(mylist,IntegerType())

print("*"*50)
df.select(avg('value')).show()
print("DF AverageResult using Dataframe")
print("*"*50)

'''
Sometimes it is useful to perform an action on all of the elements in the RDD, but without returning any result to the driver program.
A good example of this would be posting JSON to a webserver or inserting records into a database.
In either case, the foreach() action lets us perform computations on each element in the RDD without bringing it back locally.
'''
