from pyspark.sql import SparkSession


spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()
# read file.
filename='/Users/sbommireddy/Documents/python-spark-tutorial-master/in/uppercase.text'

rdd = spark.sparkContext.textFile(filename)
words = rdd.flatMap(lambda x: x.split(" "))
result = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)

print(result.take(40))
