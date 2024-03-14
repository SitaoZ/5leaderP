#TSSPlant result 

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve, auc, accuracy_score

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

def blockread(fh, sep):
    buf = ""
    while True:
        while sep in buf:
            pos = buf.index(sep)
            yield buf[:pos]
            buf = buf[pos + len(sep):]
        chunk = fh.read(4096)
        if not chunk:
            yield buf
            break
        buf += chunk

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

def roc_auc(predictions, labels):
    """

    :param predictions: predicted values
    :param labels: real values
    :return: false positive rate, true positive rate, roc_auc
    """

    fpr, tpr, thresholds = roc_curve(labels, predictions)
    auc_score = auc(fpr, tpr)
    print('threshold:', thresholds)

    return fpr, tpr, auc_score


tss_predict_label = []
tss_predict_score = []
tss_true_label = []

import re

pattern = re.compile('TSS score =  (.\d+\.\d+)')
with open('query.res', 'r') as f:
    for p in blockread(f, 'Query: >'):
        if 'Thresholds' in p:
            continue
        res_list = p.split('\n')
        # true  
        a = res_list[0].split('-')[1]
        if a == '1.0':
            tss_true_label.append(1)
        else:
            tss_true_label.append(0)
        # predict in default threshold 
        if '1 promoter(s)' in p:
            tss_predict_label.append(1)
        else:
            tss_predict_label.append(0)
        match = pattern.search(p)
        if match :
            tss_predict_score.append(float(match.group(1)))
        else:
            tss_predict_score.append(-2)

tp, tn, fp, fn = calc(tss_predict_label, tss_true_label)
acc = accuracy(tp, tn, fp, fn)
sen = sensitivity(tp, fn)
spe = specificity(tn, fp)
# roc plot 
fpr, tpr, auc_score = roc_auc(tss_predict_score, tss_true_label)
plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % auc_score)
plt.legend(loc='lower right')
plt.plot([0, 1], [0, 1], 'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate (Sensitivity)')
plt.xlabel('False Positive Rate (1-Specificity)')
plt.savefig('ROC_Curve.png')
df = pd.DataFrame(dict(fpr=fpr, tpr=tpr))
df.to_csv('ROC_Curve_data.csv', index=False)
# PR plot 
precision, recall, thresholds = precision_recall_curve(tss_true_label, tss_predict_score)
print('PR thresholds:', thresholds)
fig, ax = plt.subplots()
ax.plot(recall, precision, color='purple')
ax.set_title('Precision-Recall Curve')
ax.set_ylabel('Precision')
ax.set_xlabel('Recall')
fig.savefig('PR_Curve.png')
df = pd.DataFrame(dict(precision=precision, recall=recall))
df.to_csv('PR_Curve_data.csv', index=False)

print('tp, tn, fp, fn:', tp, tn, fp, fn)
print('accuracy:', acc)
print('sensitivity:', sen)
print('specificity:', spe)

