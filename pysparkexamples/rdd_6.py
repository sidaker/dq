from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)

#Writing a Python function which will take an character as input.
#It will return 0 if input character is a consonant otherwise 1.

def vowelCheckFunction( data) :
     if data in ['a','e','i','o','u']:
        return 1
     else :
        return 0

pythonList  =  ['b' , 'd', 'm', 't', 'e', 'u']
RDD1 = sc.parallelize(pythonList,2)
print(RDD1.collect())
print("*"*50)

#Creating a paired RDD.
RDD2 = RDD1.map( lambda data : (data, vowelCheckFunction(data)))
RDD2.collect()

#Fetching keys from paired RDD.
RDD2Keys = RDD2.keys()
print(RDD2Keys.collect())
print("*"*50)

#Step  5-1-5.  Fetching values from paired RDD.
RDD2Values = RDD2.values()
print(RDD2Values.collect())
print("*"*50)
