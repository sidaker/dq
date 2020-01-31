from pyspark.sql import SparkSession

# from pyspark import SparkContext
# spark-submit --master local sampleSpark.py
# spark-submit --master
# master node is where the cluster manager is running.
# local mode vs cluster mode
# driver runs its own Java process(JVM) so does the Executors which have their own JVM's.
# spark-submit --executor-memory 3G --total-executor-cores 2 sampleSpark.py

def splitcomma(line:str):
    splits =  line.split(",")
    # note this splits line  based on commas even if the commas are inside "" which is not we ideally want.
    # use regular expressions to handle the above mentioned situation.
    return "{},{}".format(splits[1],splits[2])

spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()
# sc = SparkContext("local[3]", "word count")

filename =  "/Users/sbommireddy/Documents/python-spark-tutorial-master/in/airports.text"

# Generate the initial RDD from external file.
#lines = spark.read.format("csv").load(sample_movielens_ratings.txt)
# read API of spark session returns a DataFrameReader that can be used to non-streaming data into dataframe.
#airports = sc.textFile(filename)
airports = spark.sparkContext.textFile(filename)

#Apply a filter Transformation.
#Goal to select only USA airports. 4th field i.e. index 3 contains Airport Country.

airportsinUSA = airports.filter(lambda line:line.split(",")[3]=="\"United States\"")


# Apply a map Transformation
# Return type of map is not necessarily same as input type.
# map returns a new RDD.
airportsNamesandCities =  airportsinUSA.map(splitcomma)

airportsNamesandCities.saveAsTextFile("/Users/sbommireddy/Documents/airports_usa.txt")
