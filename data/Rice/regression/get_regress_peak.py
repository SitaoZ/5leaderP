from math import log
import numpy as np 
import pandas as pd

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

if __name__ == '__main__':
    # norm_select.csv
    #ath = pd.read_csv('/home/zhusitao/project/DPI/01.ath/peak_process/09.jbrowser/another_regress/random_select_singleton.csv')
    #TBF1 = ath[ath.Locus == 'AT4G36990.1']
    #TBF1.to_csv('TBF1.csv', index=False)
    #ath = ath[~ath.Locus.str.contains('AT4G36990.1')]
    rice = pd.read_csv('/home/zhusitao/project/DPI/02.rice/All_isoforms_peak_process/09.jbrowser/regression/regression_data.csv')
    #cotton = pd.read_csv('/home/zhusitao/project/DPI/03.cotton/peak_process/09.jbrowser/norm_select.csv')
    #maize = pd.read_csv('/home/zhusitao/project/DPI/04.maize/peak_process/09.jbrowser/norm_select.csv')
    #soybean = pd.read_csv('/home/zhusitao/project/DPI/05.soybean/peak_process/09.jbrowser/norm_select.csv')
    #data = pd.concat([ath, rice, cotton, maize, soybean], axis=0, ignore_index=True)
    data = rice
    # data = pd.concat([ath, rice, soybean], axis=0, ignore_index=True)
    data = data[data.Seq.str.contains('N') == False]
    print(data)
    # filter region length
    # data = data[data.Label >= 150]
    # data = data[data.Label <= 150]
    # data = data[data.Peak_len < 20]
    # data = data.drop_duplicates(subset=['Locus'])
    print(data.describe())
    data.to_csv('regress_peak.csv', index=False)
    print(data.describe())
    data.loc[:, 'array'] = data.Seq.apply(seq2matrix)
    print(data.describe())
    data_array = np.rollaxis(np.array(data.array.to_list()), 1, 3)
    #label_array = np.array(data.Label.apply(lambda x:log(x+1)).to_list())
    label_array = np.array(data.Label.to_list())
    np.save('regress_data_peak', data_array)
    np.save('regress_label_peak', label_array)
