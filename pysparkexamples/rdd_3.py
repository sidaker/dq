from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()
#Create RDD of list.

pythonList = [2.3,3.4,4.3,2.4,2.3,4.0]

parPythonData = spark.sparkContext.parallelize(pythonList,2)

print("*"*50)
print(parPythonData.collect())

#Getting first element.
print("*"*50)
print(parPythonData.first())

# Getting first two elements.
print("*"*50)
print(parPythonData.take(2))

#Getting number of partitions in RDD.
print("*"*50)
print(parPythonData.getNumPartitions())
