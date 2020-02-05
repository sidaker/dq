from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()

def fahrenheitToCentigrade(temperature) :
  centigrade = (temperature-32)*5/9
  return centigrade

#  Parallelizing the data.

tempData = [59,57.2,53.6,55.4,51.8,53.6,55.4,20,33,80]
parTempData = spark.sparkContext.parallelize(tempData,2)

print("*"*50)
print(parTempData.collect())
print("*"*50)

#Converting temperature from Fahrenheit to Centigrade.
print("*"*50)
parCentigradeData = parTempData.map(fahrenheitToCentigrade)
print(parCentigradeData.collect())
print("*"*50)
#Filtering temperature greater than 13C.

def tempMoreThanThirteen(temperature):
  return temperature >=13

filteredTemprature = parCentigradeData.filter(tempMoreThanThirteen)
filteredTemprature.persist()
print("*"*50)
print(filteredTemprature.collect())
print("*"*50)

filteredTemprature = parCentigradeData.filter(lambda x : x>=18)
print("*"*50)
print(filteredTemprature.collect())
print("*"*50)

filteredTemprature = parCentigradeData.filter(lambda x : x<=9)
print("*"*50)
print(filteredTemprature.collect())
print("*"*50)

filteredTemprature.unpersist()
