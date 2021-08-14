import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# https://scikit-learn.org/stable/modules/preprocessing.html#custom-transformers
# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.FunctionTransformer.html#sklearn.preprocessing.FunctionTransformer


class TenMultiplier(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X * 10


multiplier = TenMultiplier()

X = np.array([6, 3, 7, 4, 7])
print(multiplier.transform(X))
