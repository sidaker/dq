from pyspark import SparkContext, SparkConf
# spark-submit --master local[3] accumulator_example1.py

appName="testacc"
master="local"
x = SparkConf().setAppName(appName).setMaster(master)
sc = SparkContext(conf=x)

distData = sc.parallelize(range(1000),4)

accum = sc.accumulator(0)

accum.value = accum.value + 1

print("-" *50)
print(accum.value)

#print(distData.collect())
distData.saveAsTextFile("/Users/sbommireddy/Documents/testaccum")
