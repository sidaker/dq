from pyspark.sql import SparkSession
# lets you share an immutable value efficiently across the cluser with out
# enacapsulating that value in a function enclosure.

# normal way of accesing a driver variable - Reference it in function enclsures
# e.g. inside a map function. A value will be sent everytime from driver
# to worker node tasks each time it is referenced.

# broadcast variables avoid deserializing a value multiple times(once per task)
# in a worker node.
spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()

capital_data = {"UK":"London","USA":"Washington DC", "India":"New Delhi"}

user_data = [("Sid","UK"),("Likhi","UK"), ("Bargu","USA"), ("Chikki","Australia")]

capbroadcast = spark.sparkContext.broadcast(capital_data)
# Refer the value like capbroadcast.value

# Create rdd
userrdd1 = spark.sparkContext.parallelize(user_data,2)
userrdd2 = userrdd1.map(lambda x: (x[0],capbroadcast.value.get(x[1],"no idea")))

print(type(userrdd2))
print(userrdd2.collect())
