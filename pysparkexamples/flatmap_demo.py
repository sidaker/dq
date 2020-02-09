from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()

list1 = ["Hello line1", "Welcome line2","Awesome Threesome students"]
list2 = [(1,"This is one line"),(2,"Tremendous effort twos"),(3,"Tryst with destiny mydear threes")]

def sqrt(x):
    return x*x

rdd1 = spark.sparkContext.parallelize(list1,2)
pairrdd1 = spark.sparkContext.parallelize(list2,2)

flatmapresults = rdd1.flatMap(lambda line: line.split(" ")).collect()
flatmappairresults = pairrdd1.flatMapValues(lambda line: line.split(" ")).collect()

print("*"*50)
print("using flatMap on a normal RDD")
print(flatmapresults)

print("*"*50)
print("using flatMap on a paired RDD")
print(flatmappairresults)
