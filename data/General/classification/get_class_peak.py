#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: plant.py
date: 2022/4/12 3:46 PM
author: Sitao Zhu
mail: zhusitao1990@163.com
'''


import numpy as np
import pandas as pd

def shuffle_arrays(data, label):
    """
    Shuffle data and label
    :param data: data
    :param label: label
    :return: shuffled
    """
    s = np.arange(data.shape[0]) # position array
    np.random.shuffle(s)         # shuffle
    return data[s], label[s]

def seq2matrix(seq):
    """
    ATGC sequence to one hot matrix
    :param seq: sequence
    :return: numpy matrix
    """
    matrix = np.zeros((4, len(seq)))
    seq = seq.upper()
    for pos in range(len(seq)):
        if seq[pos] == 'A':
            matrix[0, pos] = 1
        elif seq[pos] == 'C':
            matrix[1, pos] = 1
        elif seq[pos] == 'G':
            matrix[2, pos] = 1
        elif seq[pos] == 'T':
            matrix[3, pos] = 1
        else:
            continue

    return matrix

def regressData(path='/home/zhusitao/AI/TSS_Predict'):
    # data
    ath = np.load(f'{path}/ath/final_version/data/regress_data.npy')
    rice = np.load(f'{path}/rice/final_version/data/regress_data.npy')
    cotton = np.load(f'{path}/cotton/final_version/data/regress_data.npy')
    maize = np.load(f'{path}/maize/final_version/data/regress_data.npy')
    soybean = np.load(f'{path}/soybean/final_version/data/regress_data.npy')
    # label
    ath_l = np.load(f'{path}/ath/final_version/data/regress_label.npy')
    rice_l = np.load(f'{path}/rice/final_version/data/regress_label.npy')
    cotton_l = np.load(f'{path}/cotton/final_version/data/regress_label.npy')
    maize_l = np.load(f'{path}/maize/final_version/data/regress_label.npy')
    soybean_l = np.load(f'{path}/soybean/final_version/data/regress_label.npy')
    data = np.concatenate([ath, rice, cotton, maize, soybean], axis=0)
    label = np.concatenate([ath_l, rice_l, cotton_l, maize_l, soybean_l], axis=0)
    # np.array
    np.save('regress_data', data)
    np.save('regress_label', label)

def classData(path='/home/zhusitao/AI/TSS_Predict'):
    # data
    ath = np.load('/home/zhusitao/project/DPI/01.ath/All_isoforms_peak_process/09.jbrowser/classification/class_data.npy')
    rice = np.load('/home/zhusitao/project/DPI/02.rice/All_isoforms_peak_process/09.jbrowser/classification/class_data.npy')
    cotton = np.load('/home/zhusitao/project/DPI/03.cotton/All_isoforms_peak_process/09.jbrowser/classification/class_data.npy')
    maize = np.load('/home/zhusitao/project/DPI/04.maize/All_isoforms_peak_process/09.jbrowser/classification/class_data.npy')
    soybean = np.load('/home/zhusitao/project/DPI/05.soybean/All_isoforms_peak_process/09.jbrowser/classification/class_data.npy')
    # label
    ath_l = np.load('/home/zhusitao/project/DPI/01.ath/All_isoforms_peak_process/09.jbrowser/classification/class_label.npy')
    rice_l = np.load('/home/zhusitao/project/DPI/02.rice/All_isoforms_peak_process/09.jbrowser/classification/class_label.npy')
    cotton_l = np.load('/home/zhusitao/project/DPI/03.cotton/All_isoforms_peak_process/09.jbrowser/classification/class_label.npy')
    maize_l = np.load('/home/zhusitao/project/DPI/04.maize/All_isoforms_peak_process/09.jbrowser/classification/class_label.npy')
    soybean_l = np.load('/home/zhusitao/project/DPI/05.soybean/All_isoforms_peak_process/09.jbrowser/classification/class_label.npy')
    data = np.concatenate([ath, rice, cotton, maize, soybean], axis=0)
    label = np.concatenate([ath_l, rice_l, cotton_l, maize_l, soybean_l], axis=0)
    # np.array
    np.save('class_data', data)
    np.save('class_label', label)

def main():
    # regressData()
    classData()

if __name__ == '__main__':
    main()




