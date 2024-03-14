import scipy
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve, auc, accuracy_score
from sklearn.metrics import f1_score


def sensitivity(tp, fn):
    """
    Sensitivity for model
    :param tp: true positive numbers
    :param fn: false negative numbers
    :return: sensitivity
    """
    return tp/(tp+fn)


def specificity(tn, fp):
    """
    Sepcifivity for model
    :param tn: ture negative
    :param fp: false positive
    :return: specificity
    """
    return tn/(tn+fp)

def accuracy(tp, tn, fp, fn):
    """

    :param tp: true positive
    :param tn: true negative
    :param fp: false positive
    :param fn: fslse negative
    :return: accuracy
    """
    return (tp+tn)/(tp+tn+fp+fn)

def calc(predictions, labels):
    """

    :param predictions: predicted values
    :param labels:  real values
    :return: true positive, true negative, false positive, false negative
    """
    tp, tn, fp, fn = 0, 0, 0, 0
    for i in range(len(predictions)):
        result = predictions[i]
        if result == labels[i]:
            if result == 1:
                tp += 1
            else:
                tn += 1
        else:
            if result == 1:
                fp += 1
            else:
                fn += 1
    return tp, tn, fp, fn

import gzip

def true_tss(path='/home/zhusitao/project/DPI/01.ath/peak_process/09.jbrowser/robust.sort.bed.gz'):
    genome_region = {}
    # Chr1      3624    3648    p1@NAC001       282     +       3630    3631    255,0,0
    with gzip.open(path, 'rb') as f:
        for line in f:
            line = line.decode('utf:8')
            line = line.strip()
            array = line.split('\t')
            chrom, start ,end ,strand = array[0], int(array[1]), int(array[2]), array[5]
            if chrom in genome_region.keys():
                genome_region[chrom].append((start, end))
            else:
                genome_region[chrom] = [(start, end)]
    return genome_region


predict_correct = dict()
with open('../tss_start_codon.txt', 'r') as f:
    for line in f:
        line = line.strip()
        array = line.split('\t')

        chrom, tss, start_codon, locus, strand = array[0], int(array[1]), int(array[2]), array[3], array[4]
        if strand == "+":
            predict_correct[locus] = (tss, start_codon)
        else:
            predict_correct[locus] = (tss, start_codon)



tss_predict_label = []
tss_true_label = []

x = []
y = []
z = []
abs_values= []


import re

genome_region = true_tss()
with open('out.tss.bed', 'r') as f:
    for line in f:
        line = line.strip()
        # Chr1    18795221        18795222        AT1G50730.2     1       +
        array = line.split('\t')
        chrom, tss_point, locus, strand = array[0], int(array[1]), array[3], array[5]
        # 
        if not predict_correct.get(locus):
            continue
        # print(to_line[locus])
        z.append(locus)
        if strand == "+":
            tss, start_codon = predict_correct[locus]
            x.append(tss)
            y.append(tss_point)
            abs_values.append(abs(tss - tss_point))
            # print(tss, tss_point, tss - tss_point)
            if abs(tss-tss_point) <= 50:
                tss_predict_label.append(1)
            else:
                tss_predict_label.append(0)
        else:
            tss, start_codon = predict_correct[locus]
            x.append(tss)
            y.append(tss_point)
            # print(tss, tss_point, tss - tss_point)
            abs_values.append(abs(tss - tss_point))
            if abs(tss_point - tss) <= 50:
                tss_predict_label.append(1)
            else:
                tss_predict_label.append(0)

        # CAGE
        if chrom in genome_region.keys():
            switch_on = False
            for se in genome_region[chrom]:
                if se[0]<= tss_point <= se[1]:
                    tss_true_label.append(1)
                    switch_on = True
                    break
            if not switch_on:
                tss_true_label.append(0)
        else:
            tss_true_label.append(0)


print(len(tss_predict_label))
print(len(tss_true_label))

tp, tn, fp, fn = calc(tss_predict_label, tss_true_label)
acc = accuracy(tp, tn, fp, fn)
sen = sensitivity(tp, fn)
spe = specificity(tn, fp)
print(acc, sen, spe)

# print('f1-score:', f1_score(tss_true_label, tss_predict_label, average='macro'))
print('f1-score:', f1_score(tss_true_label, tss_predict_label))

print("MAE=", sum(abs_values)/len(abs_values))


def rsquared(x, y):
    """ Return R^2 where x and y are array-like."""

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    return r_value**2

df = pd.DataFrame({'prediction': y, 'true': x, 'locus': z})
df.to_csv('pred.csv', index=False)
r2 = rsquared(df.prediction, df.true)
print('r2 = ', r2)

from sklearn.metrics import mean_absolute_error as mae
print('mae=', mae(df.prediction.tolist(), df.true.tolist()))


import numpy as np
df1, df2, df3, df4, df5 = np.array_split(df, 5)
print('df1=', mae(df1.prediction.tolist(), df1.true.tolist()))
print('df2=', mae(df2.prediction.tolist(), df2.true.tolist()))
print('df3=', mae(df3.prediction.tolist(), df3.true.tolist()))
print('df4=', mae(df4.prediction.tolist(), df4.true.tolist()))
print('df5=', mae(df5.prediction.tolist(), df5.true.tolist()))

