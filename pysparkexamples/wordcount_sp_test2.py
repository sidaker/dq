# This script uses Spark Context. but use spark Session as a best practice.
# This script uses RDD's to count number of poccurenaces of each word in a file.
# Alternatively you can use SparkSQL and Dataframes to achive same result.

from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext("local[3]", "word count") # uses upto 3 cores of CPU on local machine

    sc.setLogLevel("ERROR")

    filename =  "/Users/sbommireddy/Documents/python/assignments/dq/data/pp_janeaustin.txt"
    # load the file on your local machine into an RDD. text_file is the RDD here.
    text_file = sc.textFile(filename)
    print(type(text_file)) # <class 'pyspark.rdd.RDD'>

    alt_counts = text_file.flatMap(lambda line: line.split(" ")).countByValue()

    for word, count in  alt_counts.items():
        print(word, count)
