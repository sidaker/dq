from pyspark import SparkContext
# spark-submit --executor-memory 3G --total-executor-cores 2 accumulator_example.py
sc = SparkContext("local", "Accumulator app")
'''
Accumulators are variables that are only “added” to through an associative and
 commutative operation and can therefore be efficiently supported in parallel.
 They can be used to implement counters (as in MapReduce) or sums.
  Spark natively supports accumulators of numeric types, and programmers can add
  support for new types.
'''
accum = sc.accumulator(0)
print("-" *50)
print(accum)
sc.parallelize([1, 2, 3, 4]).foreach(lambda x: accum.add(x))
print("-" *50)
print(accum)
