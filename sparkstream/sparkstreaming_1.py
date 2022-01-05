from pyspark.sql import SparkSession

'''
root@43d682bafa75:/home/workspace/spark/bin# ./spark-submit /home/workspace/hellospark.py

'''

# TO-DO: create a variable with the absolute path to the text file
# /home/workspace/Test.txt
logFile = '/home/workspace/Test.txt'

# TO-DO: create a Spark session
spark = SparkSession.builder.appName("HelloWorld").getOrCreate()

# TO-DO: set the log level to WARN
spark.sparkContext.setLogLevel('WARN')

numAs = 0
numBs = 0

def countA(row):
    '''
    Increment the counter everytime 'a' is seen in
    the row.
    '''
    global numAs
    numAs += row.value.count('a')
    print('Total As', numAs)



def countB(row):
    global numBs
    numBs += row.value.count('b')
    print('Total Bs', numBs)


# TO-DO: using the Spark session variable, call the appropriate
# function referencing the text file path to read the text file

logData = spark.read.text(logFile).cache()
### print(type(logData))
### <class 'pyspark.sql.dataframe.DataFrame'>


# TO-DO: call the appropriate function to filter the data containing
# the letter 'a', and then count the rows that were found

logData.foreach(countA)
logData.foreach(countB)
spark.stop()

# TO-DO: call the appropriate function to filter the data containing
# the letter 'b', and then count the rows that were found


# TO-DO: print the count for letter 'd' and letter 's'

# TO-DO: stop the spark application
