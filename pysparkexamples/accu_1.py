from pyspark.sql import SparkSession
# accumulators let you add data from all the tasks to a shared result.

#implement a counter to see how many of your input records failed to parse.
#Further abort processing if you see errors hitting a certain threshold.

# Allow you to update a value in a variety of trasformations and allowing
# you to efficiently transfer that value to the driver.

# mutable variable that spark can safely update on a per-row basis.
# native support for numeric types. Custom accumulators can be implemented.

# if implemented in actions, spark gurantees value updated only once.
# restarted tasks wont update the value of the accumulator.

# In transformation there is a risk of each tasks update being applied
# more than once in case of restart.

spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()
filename = "/Users/sbommireddy/Documents/python/assignments/dq/pysparkexamples/sample_zip_coty.csv"

def validaterule(line):
    zip = line.split(",")[0]
    try:
        int(zip)
    except:
        print("Invalid Zip:",zip)
        accum.add(1)


citiesrdd = spark.sparkContext.textFile(filename)

accum = spark.sparkContext.accumulator(0)

citiesrdd.foreach(lambda line: validaterule(line))

print(accum.value)
