import pandas as pd
# https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe

path = "/Users/sbommireddy/Documents/python/assignments/dq/dataformats/part-00000-be346b50-e18c-407c-bff5-b7cebc49d43a-c000.snappy.parquet"
#pandas.read_parquet(path, engine: str = 'auto', columns=None, **kwargs)
ant = pd.read_parquet(path, engine='pyarrow', columns=None)
#print(type(ant))

#print(ant.columns)
ant1 = ant.drop(['header','Minute'],axis=1)
#print(ant1.head())
#ant1.transform(lambda x: x + 1)
#print(ant1.describe)
#print(ant1.keys)
list1 = []
for label, content in ant1.items():
    # print('label:', label)
    # print('content:', content, sep='\n')
    # print("-----")
    # print(type(content))
    # print("-----")
    for i in content:
        # print(i)
        # print(type(i))
        list1.append(i)
#print(pd.DataFrame.from_records(ant1))
df1 =  pd.DataFrame.from_records(list1)
print(df1.head)
print("Number of Records ------")
print(len(df1.index))
df1.to_parquet("/Users/sbommireddy/Documents/python/assignments/dq/dataformats/zz.snappy.parquet", engine='pyarrow', compression='snappy')
# Apply function numpy.square() to square the value 2 column only i.e. with column names 'x' and 'y' only
# modDfObj = dfObj.apply(lambda x: np.square(x) if x.name in ['x', 'y'] else x)
#DataFrame.to_parquet(self, path, engine='auto', compression='snappy', index=None, partition_cols=None, **kwargs)
#ant2.to_parquet("/Users/sbommireddy/Documents/python/assignments/dq/dataformats/xx.snappy.parquet", engine='pyarrow', compression='snappy')
# pyarrow.lib.ArrowInvalid: Nested column branch had multiple children: struct<DateAcquired: string, DateofBirth: string, DeviceID: string, DocumentNumber: string, DocumentType: string, ExpirationDate: string, Forename: string, IssuingState: string, LocationID: string, Nationality: string, PlatformType: string, RecordID: string, Sex: string, Surname: string, TravelDirection: string>
