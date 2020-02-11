from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, LongType, StringType, FloatType

spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()



csvFile = spark.read.format("csv")\
  .option("header", "true")\
  .option("mode", "FAILFAST")\
  .option("inferSchema", "true")\
  .load("/Users/sbommireddy/Documents/python/Spark-The-Definitive-Guide-master/data/flight-data/csv/2010-summary.csv")


# COMMAND ----------

csvFile.write.format("csv").mode("overwrite").option("sep", "\t")\
  .save("/tmp/my-tsv-file.tsv")


# COMMAND ----------

spark.read.format("json").option("mode", "FAILFAST")\
  .option("inferSchema", "true")\
  .load("/Users/sbommireddy/Documents/python/Spark-The-Definitive-Guide-master/data/flight-data/json/2010-summary.json").show(5)


# COMMAND ----------

csvFile.write.format("json").mode("overwrite").save("/tmp/my-json-file.json")


# COMMAND ----------

spark.read.format("parquet")\
  .load("/Users/sbommireddy/Documents/python/Spark-The-Definitive-Guide-master/data/flight-data/parquet/2010-summary.parquet").show(5)


# COMMAND ----------

csvFile.write.format("parquet").mode("overwrite")\
  .save("/tmp/my-parquet-file.parquet")

#  parquet-tools schema xxx.snappy.parquet

# COMMAND ----------

spark.read.format("orc").load("/Users/sbommireddy/Documents/python/Spark-The-Definitive-Guide-master/data/flight-data/orc/2010-summary.orc").show(5)


# COMMAND ----------

csvFile.write.format("orc").mode("overwrite").save("/tmp/my-json-file.orc")
