import pandas as pd
df = pd.read_csv('/Users/sbommireddy/Downloads/test_schedules_dfds.csv')
print(df.shape[0]) #Provide the number of rows in the dataset
print(df.shape[1]) #Provide the number of columns in the dataset
print(df.isnull().mean())
print("Below Columns always have a value in the dataset")
print(df.columns[df.isnull().mean()==0])

print("Below Columns have nulls in the dataset")
print(df.columns[df.isnull().mean()!=0])
print(df.head())
df.drop(df.columns[[7]],axis=1,inplace=True ) # drop an attribute by position.
df.drop(['Unnamed: 9'], axis=1,inplace=True) # drop an attribute by name
## What happens when inplace=True is not put.
print('*'*50)
print(df.head())
print(df.columns)

## 3 core datata types in pandas. int64, float64 and object
## df composes of index, columns and data.


## indexers loc and iloc
## iloc allows numbers only. loc selects by labels and columns.

# df is 2d array and series is 1d labelled indexed array
