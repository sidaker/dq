from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
#from pyspark.sql.types import StructField, StructType, LongType, StringType, FloatType

spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()


person = spark.createDataFrame([
    (0, "Bill Chambers", 0, [100]),
    (1, "Matei Zaharia", 1, [500, 250, 100]),
    (2, "Michael Armbrust", 1, [250, 100])])\
  .toDF("id", "name", "graduate_program", "spark_status")

graduateProgram = spark.createDataFrame([
    (0, "Masters", "School of Information", "UC Berkeley"),
    (2, "Masters", "EECS", "UC Berkeley"),
    (1, "Ph.D.", "EECS", "UC Berkeley")])\
  .toDF("id", "degree", "department", "school")

sparkStatus = spark.createDataFrame([
    (500, "Vice President"),
    (250, "PMC Member"),
    (100, "Contributor")])\
  .toDF("id", "status")


# COMMAND ----------

joinExpression = person["graduate_program"] == graduateProgram['id']


# COMMAND ----------

wrongJoinExpression = person["name"] == graduateProgram["school"]


# COMMAND ----------

joinType = "inner"


# COMMAND ----------

gradProgram2 = graduateProgram.union(spark.createDataFrame([
    (0, "Masters", "Duplicated Row", "Duplicated School")]))

gradProgram2.createOrReplaceTempView("gradProgram2")


# COMMAND ----------

person.withColumnRenamed("id", "personId")\
  .join(sparkStatus, expr("array_contains(spark_status, id)")).show()

# Does not have to be an exact equal condition. Any boolean expression
# that results in True condition will be fine for Join.
# 

# COMMAND ----------
graduateProgram.createOrReplaceTempView("graduateProgram")
person.createOrReplaceTempView("person")

print("*"*50)
print("using normal Join or Inner join")
innerjoin_df1 = spark.sql("""
SELECT * FROM person JOIN graduateProgram
  ON person.graduate_program = graduateProgram.id
""")
innerjoin_df1.show()

print("*"*50)
print("using outer Join or Full outer  join")
outerjoin_df2 = spark.sql("""
SELECT * FROM person FULL OUTER JOIN graduateProgram
  ON graduate_program = graduateProgram.id
""")
outerjoin_df2.show()

print("*"*50)
print("using left Join or left outer join")
leftjoin_df3 = spark.sql("""
SELECT * FROM graduateProgram LEFT OUTER JOIN person
  ON person.graduate_program = graduateProgram.id
""")
leftjoin_df3.show()

print("*"*50)
print("using right Join or right outer join")
rightouterjoin_df4 = spark.sql("""
SELECT * FROM person RIGHT OUTER JOIN graduateProgram
  ON person.graduate_program = graduateProgram.id
""")
rightouterjoin_df4.show()

print("*"*50)
print("using left semi join")
# No values included from right dataframe.
leftsemijoin_df5 = spark.sql("""
SELECT * FROM gradProgram2 LEFT SEMI JOIN person
  ON gradProgram2.id = person.graduate_program
""")
leftsemijoin_df5.show()

print("*"*50)
print("using left ANTI join")
# Rows only in left table
leftantijoin_df6 = spark.sql("""
SELECT * FROM graduateProgram LEFT ANTI JOIN person
  ON graduateProgram.id = person.graduate_program
""")
leftantijoin_df6.show()


print("*"*50)
print("using natural Join")
naturaljoin_df7 = spark.sql("""
SELECT * FROM graduateProgram NATURAL JOIN person
""")
naturaljoin_df7.show()

print("*"*50)
print("using CROSS join")
crossjoin_df7 = spark.sql("""
SELECT * FROM graduateProgram CROSS JOIN person
  ON graduateProgram.id = person.graduate_program
""")
crossjoin_df7.show()
