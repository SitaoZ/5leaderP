#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: train_utils.py
date: 2021/12/27 下午2:39
author: Sitao Zhu
mail: zhusitao1990@163.com
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, accuracy_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import f1_score
import scipy.stats as stats

def sensitivity(tp, fn):
    """
    Sensitivity formula
    :param tp: true positive numbers
    :param fn: false negative numbers
    :return: sensitivity
    """
    return tp/(tp+fn)


def specificity(tn, fp):
    """
    Sepcifivity formula
    :param tn: ture negative
    :param fp: false positive
    :return: specificity
    """
    return tn/(tn+fp)


def calc(predictions, labels):
    """
    :param predictions: predicted values
    :param labels:  real values
    :return: true positive, true negative, false positive, false negative
    """
    tp, tn, fp, fn = 0, 0, 0, 0
    for i in range(len(predictions)):
        result = 1 if predictions[i] >= 0.5 else 0
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
    The auc_score calculate
    :param predictions: predicted values
    :param labels: real values
    :return: false positive rate, true positive rate, roc_auc
    """

    fpr, tpr, thresholds = roc_curve(labels, predictions)
    auc_score = auc(fpr, tpr)

    return fpr, tpr, auc_score

def roc_curves(predictions, labels, fold=1):
    """
    Calculate ROC Curve for fold and save file
    :param predictions: predictions
    :param labels: labels
    :param fold: ten cross fold
    :return: None
    """
    fpr, tpr, auc_score = roc_auc(predictions, labels)
    # plot
    fig, ax = plt.subplots()
    ax.plot(fpr, tpr, 'b', label='Fold%d AUC = %0.2f' % (fold, auc_score))
    ax.set_title('Receiver Operating Characteristic')
    ax.set_ylabel('True Positive Rate (Sensitivity)')
    ax.set_xlabel('False Positive Rate (1-Specificity)')
    ax.legend(loc='lower right')
    ax.plot([0, 1], [0, 1], 'r--')
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    fig.savefig('ROC_Curve_fold%d.png'%(fold))
    # data for ggplot2 in R
    df = pd.DataFrame(dict(fpr=fpr, tpr=tpr))
    df.to_csv('ROC_Curve_fold%d_data.csv'%(fold), index=False)


def pr(predictions, labels):
    """
    Precision-Recall calculate
    :param predictions: predictions
    :param labels: labels
    :return: precision, recall, thresholds
    """
    precision, recall, thresholds = precision_recall_curve(labels, predictions)
    return precision, recall, thresholds

def pr_curves(predictions, labels, fold=1):
    """
    Calculate PR Curve for fold and save file
    :param predictions:
    :param labels:
    :param fold:
    :return:
    """
    precision, recall, thresholds = precision_recall_curve(labels, predictions)
    fig, ax = plt.subplots()
    ax.plot(recall, precision, color='purple')
    ax.set_title('Precision-Recall Curve')
    ax.set_ylabel('Precision')
    ax.set_xlabel('Recall')
    fig.savefig('PR_Curve_fold%d.png'%(fold))
    df = pd.DataFrame(dict(precision=precision, recall=recall))
    df.to_csv('PR_Curve_fold%d_data.csv'%(fold), index=False)

def accuracy(tp, tn, fp, fn):
    """
    Accuracy calculate
    :param tp: true positive
    :param tn: true negative
    :param fp: false positive
    :param fn: fslse negative
    :return: accuracy
    """
    return (tp+tn)/(tp+tn+fp+fn)

def acc_score(predictions, labels):
    """
    Calculate accuracy
    :param predictions: predicted values
    :param labels: real values
    :return: accuracy
    """
    tp, tn, fp, fn = calc(predictions, labels)
    acc = accuracy(tp, tn, fp, fn)
    return acc


def all_class_metrics(predictions, true):
    """
    :param predictions: predicted values
    :param true: true values
    :return: print all metrics
    """
    tp, tn, fp, fn = calc(predictions, true)
    print('TP:', tp, '; TN:', tn, '; FP:', fp, '; FN:', fn)
    print('Accuracy:', accuracy(tp, tn, fp, fn))
    print('Sensetivity:', sensitivity(tp, fn))
    print('Specificity:', specificity(tn, fp))
    print('AUC:', roc_auc(predictions, true)[2])


def f1(predictions, true):
    """
    f1_score = 2*(precision*recall)/(precision + recall)
    :param predictions:
    :param true:
    :return:
    """
    tp, tn, fp, fn = calc(predictions, true)
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1score = 2 * (precision * recall)/(precision + recall)
    return f1score


def mse(predictions, labels):
    """
    :param predictions: predicted values
    :param true: label value
    :return:
    """
    return np.mean((predictions.squeeze() - labels) ** 2)


def rmse(predictions, labels):
    """
    :param predictions: predicted values
    :param labels: label value
    :return:rooted mean squared error or mean absolute error
    """
    return np.mean(((predictions.squeeze() - labels) ** 2) ** 0.5)

def r_square(predictions, labels):
    """
    R-square scaculate and save for plot
    :param predictions: pedicted values
    :param labels: label value
    :return: R2
    """
    slope, intercept, rvalue, pvalue, stderr = stats.linregress(predictions, labels)
    df = pd.DataFrame(dict(predict=predictions, label=labels))
    df.to_csv('r_square.csv', index=False)
    return rvalue ** 2