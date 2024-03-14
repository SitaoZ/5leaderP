#TSSPlant result 

import re
import scipy
from scipy import stats
import pandas as pd 

result = dict()
Label = []
x = []
y = []

P = 0
pattern = re.compile('TSS position:(\s+)(\d+)')
with open('query.res', 'r') as f, open('reg_df.csv', 'w') as out:
    print(*['locus', 'true', 'prediction'], file=out, sep=',')
    for i, line in enumerate(f):
        line = line.strip()
        if 'Query: >' in line:
            array = line.split(" ")[1].split("_")
            locus, position = array[0], array[1]
            locus = locus.replace(">", "")
            Label.append((locus, position))
            P = i
            result[P] = (locus, position)
        if "TSS position" in line and i - 10 == P:
            matched = pattern.search(line)
            locus, position = result[P]
            x.append([position])
            print(*[locus, position, abs(int(matched.group(2))-256)], file=out, sep=',')
            y.append([matched.group(2)])
            

def rsquared(x, y):
    """ Return R^2 where x and y are array-like."""

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    return r_value**2
df = pd.read_csv('reg_df.csv')
r2 = rsquared(df.prediction, df.true)
print('r2 = ', r2)

from sklearn.metrics import mean_absolute_error as mae
print(mae(df.prediction.tolist(), df.true.tolist()))

import numpy as np 
df1, df2, df3, df4, df5 = np.array_split(df, 5)
#print(df1)
print('df1=', mae(df1.prediction.tolist(), df1.true.tolist()))
print('df2=', mae(df2.prediction.tolist(), df2.true.tolist()))
print('df3=', mae(df3.prediction.tolist(), df3.true.tolist()))
print('df4=', mae(df4.prediction.tolist(), df4.true.tolist()))
print('df5=', mae(df5.prediction.tolist(), df5.true.tolist()))
