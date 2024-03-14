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

def classData(path='predict_result.csv'):
    """
    concat five species classifier training data
    :param path:
    :return:
    """
    df = pd.read_csv(path)
    # np.array
    class_data = np.array(df.Seqs.apply(seq2matrix).to_list())
    class_data = np.rollaxis(class_data, 1, 3)
    class_label = np.array(df.Label)
    # shuffle 
    class_data, class_label = shuffle_arrays(class_data, class_label)
    np.save('test_class_data', class_data)
    np.save('test_class_label', class_label)


def main():
    classData()

if __name__ == '__main__':
    main()




