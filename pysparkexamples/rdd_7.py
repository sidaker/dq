from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf = conf)

studentMarksData = [["Sid","year1",62.08,62.4],
  ["Sid","year2",75.94,76.75],
  ["Likhi","year1",68.26,72.95],
  ["Likhi","year2",85.49,75.8],
  ["Bargu","year1",75.08,79.84],
  ["Bargu","year2",54.98,87.72],
  ["Chikki","year1",50.03,66.85],
  ["Chikki","year2",71.26,69.77],
  ["Poorguy","year1",52.74,76.27],
  ["Poorguy","year2",50.39,68.58],
  ["Avgguy","year1",74.86,60.8],
  ["Avgguy","year2",58.29,62.38],
  ["Advik","year1",93.95,94.51],
  ["Advik","year2",96.69,96.92]]

studentMarksDataRDD = sc.parallelize(studentMarksData,4)
#Calculating average year wise marks.

studentMarksMean = studentMarksDataRDD.map(lambda x : [x[0],x[1],(x[2]+x[3])/2])
studentMarksMean.persist()
print("*"*50)
print("Average Marks for each year for two students")
print(studentMarksMean.take(2))

#Filtering student average marks in second year.
secondYearMarks = studentMarksMean.filter(lambda x : "year2" in x)
print("*"*50)
print("Average Marks for 2nd year for two students")
print(secondYearMarks.take(2))

studentMarksMean.unpersist()

#Top 3 students who has scored highest average marks in second year.
sortedMarksData = secondYearMarks.sortBy(keyfunc = lambda x : -x[2])
#sortedMarksData.collect()
print("Using sortBy which is a transformation")
print("*"*50)
print(sortedMarksData.take(3))

print("*"*50)
print("Using take ordered which is an action")
topThreeStudents = secondYearMarks.takeOrdered(num=3, key = lambda x :-x[2])
print(topThreeStudents)


#Bottom 3 students who has scored lowest average marks in second year.
print("*"*50)
print("Bottom 3 students")
bottomThreeStudents = secondYearMarks.takeOrdered(num=3, key = lambda x :x[2])
print(bottomThreeStudents)

#Get all the student who has secured more than 80% average marks in second semester of second year.
moreThan80Marks = secondYearMarks.filter(lambda x : x[2] > 80)
print("*"*50)
print("More than 80 percent in 2nd year")
print(moreThan80Marks.collect())
