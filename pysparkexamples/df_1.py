from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, LongType, StringType, FloatType

# from pyspark import SparkContext
# spark-submit --master local sampleSpark.py
# spark-submit --master
# master node is where the cluster manager is running.
# local mode vs cluster mode
# driver runs its own Java process(JVM) so does the Executors which have their own JVM's.
# spark-submit --executor-memory 3G --total-executor-cores 2 sampleSpark.py


spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()

filename =  "/Users/sbommireddy/Documents/python-spark-tutorial-master/in/airports.text"

myManualSchema = StructType([
StructField("AirportId",LongType(),True),
StructField("AirportName",StringType(),True),
StructField("City",StringType(),True),
StructField("Country",StringType(),True),
StructField("AirportCode",StringType(),True),
StructField("ICAOCode",StringType(),True),
StructField("Latitude",FloatType(),False),
StructField("Longitude",FloatType(),False),
StructField("Altitude",FloatType(),False),
StructField("timezoneDST",StringType(),False),
StructField("unknown",StringType(),False),
StructField("timeZoneinOlson",StringType(),False)
])

airports = spark.read.format("csv").schema(myManualSchema).load(filename)
# option("inferSchema", "true").option("header","true")
print(airports.rdd.getNumPartitions)
# Each partition is a separate CSV file when you write a DataFrame to disk.

# make the dataframe a table or view.
airports.createOrReplaceTempView("airports_all")

airportsNamesandCities = spark.sql("""
SELECT AirportName,City
FROM airports_all
WHERE Country = "United States"
""")

airportsNamesandCities.show()
