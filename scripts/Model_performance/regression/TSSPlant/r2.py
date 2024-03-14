import scipy
from sklearn.metrics import r2_score
import pandas as pd 

def r_squared(y, y_hat):
    y_bar = y.mean()
    ss_tot = ((y-y_bar)**2).sum()
    ss_res = ((y-y_hat)**2).sum()
    return 1 - (ss_res/ss_tot)

def rsquared(x, y):
    """ Return R^2 where x and y are array-like."""

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    return r_value**2

for i in range(10):
    df = pd.read_csv(f'/home/zhusitao/AI/TSS_Predict/ath/regression/prediction_interval_fold{i}.csv')
    # r2 = r2_score(df.prediction, df.true)
    r2 = rsquared(df.prediction, df.true)
    print(f'fold{i} r2=',r2)


from sklearn.metrics import mean_absolute_error as mae

print(mae(df.prediction.tolist(), df.true.tolist()))
