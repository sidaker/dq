import pandas as pd
import os
from sklearn import tree
# https://archive.ics.uci.edu/ml/datasets/student+performance#
dir = '/Users/sbommireddy/Downloads/student/'
por_file =  os.path.join(dir,'student-por.csv')
out_file =  os.path.join(dir,'sid-student-per.dot')

# Read the CSV into a pandas dataframe.
d = pd.read_csv(por_file, sep=';')
#print(len(d))
#print(d.head())

d['pass'] = d.apply(lambda row:1 if(row['G1']+row['G2']+row['G3']) >= 35 else 0, axis =1)
d = d.drop(['G1','G2','G3'], axis =1 )
# axis=1 means use apply per row and axis=0 would mean apply per column
print(d.head())

print(d.columns)

# use one-hot encoding on categorical columns

d = pd.get_dummies(d, columns=['sex', 'school', 'address',
'famsize','Pstatus', 'Mjob','Fjob','reason','guardian',
'schoolsup','famsup' , 'paid', 'activities','nursery' ,
'higher' , 'internet', 'romantic'])

print(d.head())
print(d.columns)

# shuffle and select  500 rows for training and 249 for test.
d = d.sample(frac=1) # This can be 0.5 if you only want to select 50%.

##print(len(d.sample(frac=0.5))) # 324

d_train = d[:500]
d_test = d[500:]

d_train_attr = d_train.drop(['pass'],axis=1)
d_train_pass = d_train['pass']

d_test_attr = d_test.drop(['pass'],axis=1)
d_test_pass = d_test['pass']

# DecisionTreeClassifier  from scikit learn.
# Perform multi class classification.

# We will split at a depth of five questions, by using max_depth=5 as an initial tree depth to get a feel for how the tree is fitting the data

t = tree.DecisionTreeClassifier(criterion="entropy",max_depth=3)
t = t.fit(d_train_attr,d_train_pass)

# save tree.
tree.export_graphviz(t,out_file=out_file,label=all,impurity=False,
proportion=True,feature_names=list(d_train_attr),class_names=["fail","pass"],
filled=True,rounded=True)

print(t.score(d_test_attr,d_test_pass))
