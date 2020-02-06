from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()

def fahrenheitToCentigrade(temperature) :
  centigrade = (temperature-32)*5/9
  return centigrade

#  Parallelizing the data.

tempData = [59,57.2,53.6,55.4,51.8,53.6,55.4,20,33,80,70,43,90]
parTempData = spark.sparkContext.parallelize(tempData,2)

print("*"*50)
print(parTempData.collect())
print("*"*50)

#Converting temperature from Fahrenheit to Centigrade.
print("*"*50)
parCentigradeData = parTempData.map(fahrenheitToCentigrade)
parCentigradeData.persist()
print(parCentigradeData.collect())
print("*"*50 + "Converted F to C")
print("*"*50)
#Filtering temperature greater than 13C.

def tempMoreThanThirteen(temperature):
  return temperature >=13

print("*"*50)
print(parCentigradeData.filter(tempMoreThanThirteen).collect())
print("*"*50)

print(parCentigradeData.filter(lambda x : x>=18).collect())
print("*"*50)

print(parCentigradeData.filter(lambda x : x<=9).collect())
print("*"*50)
parCentigradeData.unpersist()
