from sklearn.metrics import mean_absolute_error as mae
import pandas as pd 

# 对应到预测的TSS位点和一致的TSS位点的距离 MAE


# lower,prediction,upper,true,Seq,Locus,Label,Peak_len,Peak_start,Peak_end,Peak_point,TS_Start,TS_End,Longest_Prominent,predict_peak
# tbf_pred = pd.read_csv('predict_peak.csv')
tbf_pred = pd.read_csv('predict_again.csv')

print(mae(tbf_pred.prediction.tolist(),tbf_pred.Label.tolist()))


import numpy as np
df1, df2, df3, df4, df5 = np.array_split(tbf_pred, 5)
#print(tbf_pred.shape)
#print(df1.shape)
#print(df2.shape)
#print(df3.shape)
#print(df4.shape)
#print(df5.shape)
print('df1=', mae(df1.prediction.tolist(), df1.Label.tolist()))
print('df2=', mae(df2.prediction.tolist(), df2.Label.tolist()))
print('df3=', mae(df3.prediction.tolist(), df3.Label.tolist()))
print('df4=', mae(df4.prediction.tolist(), df4.Label.tolist()))
print('df5=', mae(df5.prediction.tolist(), df5.Label.tolist()))
