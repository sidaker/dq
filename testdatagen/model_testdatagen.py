#from faker import Faker
import json            # To create a json file
import numpy as np
import pandas as pd
#fake = Faker('en_GB')

def create_data(x):

    # dictionary
    model_data ={}
    for i in range(0, x):

        model_data[i]={}
        model_data[i]['segment']= 'Customer'
        model_data[i]['field']= pd.util.testing.rands(3)
        model_data[i]['random_attrib']= pd.util.testing.rands(3)
        model_data[i]['msisdn']= "07{}{}{}{}{}{}{}{}{}".format(np.random.randint(0,9), np.random.randint(0,9), np.random.randint(0,9), 0, 0, 0, np.random.randint(0,9), np.random.randint(0,9), np.random.randint(0,9))
        model_data[i]['PROPENSITY'] = np.random.random()
        model_data[i]['TOP_PERCENTILE'] = np.random.randint(30,100)

    return model_data

model = create_data(10)
#print(pd.DataFrame.from_dict(model))

print(model)

print(pd.DataFrame.from_dict(model).T)
pd.DataFrame.from_dict(model).T.to_csv('testmodel.csv',index=False)
