from pyspark.sql import SparkSession
from pyspark.sql.types import Row
# Createas a parquet file and loads an input file into it
# For input you can use files/favourite_animal.csv as the iput
#from pyspark import SparkContext
#from pyspark.sql import SQLContext
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Error usage: Load [sparkmaster] [inputFile] [parquetfile]")
        sys.exit(-1)
    master = sys.argv[1]
    inputFile = sys.argv[2]
    parquetFile = sys.argv[3]
    spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()

    # Load some data into an RDD
    rdd = spark.sparkContext.textFile(inputFile).map(lambda l: l.split(","))
    namedRdd = rdd.map(lambda r: {"name": r[0], "favouriteAnimal": r[1]})
    print(namedRdd.collect())

    """
    UserWarning: Using RDD of dict to inferSchema is deprecated.
    Use pyspark.sql.Row instead
    """
    print("*"*50)
    print("Deprecated method")
    myDF = spark.createDataFrame(namedRdd)
    myDF.printSchema()

    print("*"*50)
    print("method 1 convert RDD to DF")
    myDF1 = spark.createDataFrame(rdd,["name", "favouriteAnimal"])
    myDF1.printSchema()

    # Save it
    #schemaNamedRdd.saveAsParquetFile(parquetFile)
