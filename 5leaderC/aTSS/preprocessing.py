#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: preprocessing.py
date: 2022/2/28 10:13 PM
author: Sitao Zhu
mail: zhusitao1990@163.com
'''
import os
import sys
import time
import random
import argparse
import numpy as np
import pandas as pd
from Bio import SeqIO
from random import randint


def seqFilter(seq, chars=['N','Y','S','K','R','W']):
    """
    Remove none[ATGC] characters
    :param seq: sequence
    :param Non_chars: character removed
    :return:
    """
    if any(char in seq for char in chars):
        # contain all non char
        return False
    else:
        # not contain
        return True


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


def matrix2seq(numpy_matrix):
    """
    Numpy Matrix to sequence
    :param numpy_matrix: matrix
    :return: seq string
    """
    n, c, l = numpy_matrix.shape
    charar = np.chararray((n, l), unicode=True)
    charar[:] = 'N'

    charar[np.where(numpy_matrix[:, 0, :] == 1)] = 'A'
    charar[np.where(numpy_matrix[:, 1, :] == 1)] = 'C'
    charar[np.where(numpy_matrix[:, 2, :] == 1)] = 'G'
    charar[np.where(numpy_matrix[:, 3, :] == 1)] = 'T'
    seq = np.array([])
    for i in range(n):
        seq = np.append(seq, ''.join(charar[i]))
    return seq


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

