'''
Structured API's are high level.
Use them to manipulate all sort sof data, CSV, Parquet.
Three Core ttypes of API's
    - Datasets
    - Dataframes
    - SQL tables and views
'''

'''
Both Datasets and Dataframes are distributed table like collections with well defined rows  and tables.
'''
spark.range(2).collect()

myRange = spark.range(100).toDF("number")
myRange.printSchema()
# toDF() provides a concise syntax for creating DataFrames
# The toDF() method can be called on a sequence object to create a DataFrame.

# COMMAND ----------

divisBy2 = myRange.where("number % 2 = 0")
divisBy2.collect()

myRange.select(myRange["number"] + 10 )
myRange.select(myRange["number"] + 10 ).collect()
'''
Two things to # NOTE:
1. Addition happens because Spark will convert an expression written in
Python to Spark Catalyst representation of that same type information
'''

 # COMMAND ----------

flightData2015 = spark\
  .read\
  .option("inferSchema", "true")\
  .option("header", "true")\
  .csv("/Users/sbommireddy/Documents/python/Spark-The-Definitive-Guide-master/data/flight-data/csv/2015-summary.csv")

  # COMMAND ----------

flightData2015.createOrReplaceTempView("flight_data_2015")


# COMMAND ----------

sqlWay = spark.sql("""
SELECT DEST_COUNTRY_NAME, count(1)
FROM flight_data_2015
GROUP BY DEST_COUNTRY_NAME
""")

dataFrameWay = flightData2015\
  .groupBy("DEST_COUNTRY_NAME")\
  .count()

sqlWay.explain()
dataFrameWay.explain()


# COMMAND ----------

from pyspark.sql.functions import max

flightData2015.select(max("count")).take(1)


# COMMAND ----------

maxSql = spark.sql("""
SELECT DEST_COUNTRY_NAME, sum(count) as destination_total
FROM flight_data_2015
GROUP BY DEST_COUNTRY_NAME
ORDER BY sum(count) DESC
LIMIT 5
""")

maxSql.show()


# COMMAND ----------

from pyspark.sql.functions import desc

flightData2015\
  .groupBy("DEST_COUNTRY_NAME")\
  .sum("count")\
  .withColumnRenamed("sum(count)", "destination_total")\
  .sort(desc("destination_total"))\
  .limit(5)\
  .show()


# COMMAND ----------

flightData2015\
  .groupBy("DEST_COUNTRY_NAME")\
  .sum("count")\
  .withColumnRenamed("sum(count)", "destination_total")\
  .sort(desc("destination_total"))\
  .limit(5)\
  .explain()


spark.sql("""
SELECT DEST_COUNTRY_NAME, count
FROM flight_data_2015
LIMIT 5
""").show()

spark.sql("""
SELECT  count(*)
FROM flight_data_2015
""").show()

spark.sql("""
SELECT  *
FROM flight_data_2015
""").show()

spark.sql("""
SELECT  *
FROM flight_data_2015
""").collect()
