# Creating a SparkSession in Python
# spark-submit --master local example_sp1.py
from pyspark.sql import SparkSession


spark = SparkSession.builder.master("local").appName("Word Count")\
        .getOrCreate()


# COMMAND ----------

df1 = spark.range(2, 10000, 2)
df2 = spark.range(2, 10000, 4)
step1 = df1.repartition(5)
step12 = df2.repartition(6)
step2 = step1.selectExpr("id * 5 as id")
step3 = step2.join(step12, ["id"])
step4 = step3.selectExpr("sum(id)")

a_var = step4.collect()
print(a_var)
