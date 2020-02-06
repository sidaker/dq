from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)

studentMarksDataRDD = sc.parallelize(range(1,200000),4)

print("*"*50)
print(studentMarksDataRDD.getNumPartitions())
print("*"*50)

repartstudentMarksDataRDD = studentMarksDataRDD.repartition(8)

print("*"*50)
print(repartstudentMarksDataRDD.getNumPartitions())
print("*"*50)

repartstudentMarksDataRDD.persist()

totalsum = repartstudentMarksDataRDD.reduce(lambda x,y:x+y)
print(totalsum)
print("*"*50)
