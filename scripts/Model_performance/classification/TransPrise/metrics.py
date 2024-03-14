"""
Metrics for training and prediction
"""
from sklearn.metrics import roc_curve, auc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import precision_recall_curve

def sensetivity(tp, fn):
    """
    
    :param tp: true positives results
    :param fn: false negative results
    :return: sensetivity
    """
    return tp/(tp + fn)


def specificity(tn, fp):
    """
    
    :param tn: true negative results
    :param fp: false positive results
    :return: specificity
    """

    return tn/(tn+fp)


def accuracy(tp, tn, fp, fn):
    """
    
    :param tp: true positives results
    :param tn: true negatives results
    :param fp: false positives results
    :param fn: false negatives results
    :return: accuracy
    """

    return (tp+tn)/(tp+tn+fp+fn)


def results(predictions, true):
    """
    
    :param predictions: predicted values
    :param true: real values
    :return: true positives, true negatives, false positives, false negatives
    """
    tp, tn, fp, fn = 0, 0, 0, 0

    for i in range(len(predictions)):
        result = 1 if predictions[i] >= 0.5 else 0
        if result == true[i]:
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


def cc(tp, tn, fp, fn):
    """
    
    :param tp: true positives results
    :param tn: true negatives results
    :param fp: false positives results
    :param fn: false negatives results
    :return: correlation coefficient
    """

    return (tp*tn - fp*fn)/((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))**0.5


def roc_auc(predictions, true):
    """
    
    :param predictions: predicted values
    :param true: true values
    :return: false positive rate, true positive rate, roc_auc
    """

    fpr, tpr, thresholds = roc_curve(true, predictions)
    auc_score = auc(fpr, tpr)

    return fpr, tpr, auc_score

def roc_curves(predictions, labels):
    # calculate the fpr and tpr for all thresholds of the classification
    fpr, tpr, auc_score = roc_auc(predictions, labels)
    # plot
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % auc_score)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate (Sensitivity)')
    plt.xlabel('False Positive Rate (1-Specificity)')
    plt.savefig('ROC_Curve.png')
    # data for ggplot2 in R
    df = pd.DataFrame(dict(fpr=fpr, tpr=tpr))
    df.to_csv('ROC_Curve_data.csv', index=False)

def pr_curves(predictions, labels):
    precision, recall, thresholds = precision_recall_curve(labels, predictions)
    fig, ax = plt.subplots()
    ax.plot(recall, precision, color='purple')
    ax.set_title('Precision-Recall Curve')
    ax.set_ylabel('Precision')
    ax.set_xlabel('Recall')
    fig.savefig('PR_Curve.png')
    df = pd.DataFrame(dict(precision=precision, recall=recall))
    df.to_csv('PR_Curve_data.csv', index=False)

def mse(predictions, test_answers):
    """
    
    :param predictions: predicted values
    :param test_answers: real values
    :return: mean squared error
    """

    return np.mean((predictions.squeeze() - test_answers) ** 2)


def rmse(predictions, true):
    """
    
    :param predictions: predicted values
    :param true: real values
    :return: rooted mean squared error or mean absolute error
    """

    return np.mean(((predictions.squeeze() - true) ** 2) ** 0.5)


def all_class_metrics(predictions, true):
    """
    
    :param predictions: predicted values
    :param true: true values
    :return: print all metrics
    """

    tp, tn, fp, fn = results(predictions, true)
    print('TP:', tp, '; TN:', tn, '; FP:', fp, '; FN:', fn)
    print('Accuracy:', accuracy(tp, tn, fp, fn))
    print('Sensetivity:', sensetivity(tp, fn))
    print('Specificity:', specificity(tn, fp))
    print('Correlation coefficient:', cc(tp, tn, fp, fn))
    print('AUC:', roc_auc(predictions, true)[2])
