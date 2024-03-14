import numpy as np 
import pandas as pd

pr = pd.read_csv('PR_Curve_data_TransPrise.csv')
recall =  []
precision = []
for i in range(len(pr.values)):
    if i == 0 :
        continue
    if i%10 == 0:
        n = i/10
        start = int((n-1)*10)
        end = i
        port = pr.values[start:end,:]
        port_mean = port.mean(axis=0)
        recall.append(port_mean[0])
        precision.append(port_mean[1])

new_pr = pd.DataFrame({'recall': recall, 'precision': precision})
new_pr.to_csv('PR_Curve_data_TransPrise_new.csv', index=False)
