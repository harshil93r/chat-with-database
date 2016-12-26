from pandas import DataFrame
from math import log

df = DataFrame.from_csv("data2cluster.txt", sep="\t")

import scipy.cluster.hierarchy as hc

dfVal = df.values

Z = hc.linkage(expVals, metric='euclidean', method='single')