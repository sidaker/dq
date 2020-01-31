from pyspark.sql import SparkSession
# spark-submit --master local sampleSpark.py
# spark-submit --master
# master node is where the cluster manager is running.
# local mode vs cluster mode
# driver runs its own Java process(JVM) so does the Executors which have their own JVM's.
# spark-submit --executor-memory 3G --total-executor-cores 2 sampleSpark.py

spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()

filename='/Users/sbommireddy/Documents/python/assignments/dq/test/bitd_1k.csv'

df=spark.read.csv(filename,header=True).toDF
