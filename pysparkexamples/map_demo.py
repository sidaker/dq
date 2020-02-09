from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()

list1 = [1,2,3,4,5,6]
list2 = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6)]

def sqrt(x):
    return x*x

rdd1 = spark.sparkContext.parallelize(list1,2)
pairrdd1 = spark.sparkContext.parallelize(list2,2)

maprdd1 = rdd1.map(sqrt).collect()

print("*"*50)
print("using map on a normal RDD")
print(maprdd1)

print("*"*50)
print("using map on a paired RDD")
mappairresults = pairrdd1.map(lambda x:(x[0],sqrt(x[1]))).collect()
print(mappairresults)

print("*"*50)
print("using mapValues on a paired RDD")
mapvaluespairresults = pairrdd1.mapValues(lambda x:sqrt(x)).collect()
print(mapvaluespairresults)
