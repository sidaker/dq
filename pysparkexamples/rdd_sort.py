Custom sort order in Python, sorting integers as if strings
rdd.sortByKey(ascending=True, numPartitions=None, keyfunc = lambda x: str(x))
