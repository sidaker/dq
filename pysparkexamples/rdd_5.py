from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('mytestSparkapp').getOrCreate()

# Parallelizing the data.

airVelocityKMPH = [12,13,15,12,11,12,11]
# create RDD.
parVelocityKMPH = spark.sparkContext.parallelize(airVelocityKMPH,2)
# Persist RDD
parVelocityKMPH.persist()
#Number of data points.

countDataPoints =  parVelocityKMPH.count()
print(countDataPoints)
print("*"*50)

#Summation of air velocities over day.
sumValue =  parVelocityKMPH.sum()
print(sumValue)
print("*"*50)

#Mean air velocity over day.
meanValue =  parVelocityKMPH.mean()
print(meanValue)
print("*"*50)

#Step 4-5-5. Variance of air data.
varianceValue = parVelocityKMPH.variance()
print(varianceValue)
print("*"*50)

#Step 4-5-6.  Sample Variance
sampleVarianceValue =  parVelocityKMPH.sampleVariance()
print(sampleVarianceValue)
print("*"*50)

#Step 4-5-7.  Standard Deviation
stdevValue = parVelocityKMPH.stdev()
print(stdevValue)
print("*"*50)

#Step 4-5-8. Sample Standard Deviation
sampleStdevValue = parVelocityKMPH.sampleStdev()
print(sampleStdevValue)
print("*"*50)

#Step 4-5-9. Calculating all in one step
print(parVelocityKMPH.stats())
parVelocityKMPH.stats().asDict()
parVelocityKMPH.stats().mean()
parVelocityKMPH.stats().stdev()
parVelocityKMPH.stats().count()
parVelocityKMPH.stats().min()
print(parVelocityKMPH.stats().max())
print("*"*50)
parVelocityKMPH.unpersist()
