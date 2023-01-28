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
    regress = pd.read_csv('positive_data.csv')
    positive = regress[['Locus','Seq']]
    positive.loc[:,'Label'] = 1
    negative = pd.read_csv('negative_data.csv')
    negative.columns = ['Locus', 'Seq']
    negative.loc[:,'Label'] = 0
    negative_trunct = negative.sample(n=positive.shape[0], random_state=1)
    data = pd.concat([positive, negative_trunct], axis=0)    
    data.to_csv('classData.csv', index=False)
    data = pd.read_csv('classData.csv')    
    data.loc[:, 'array'] = data.Seq.apply(seq2matrix)
    print(np.array(data.array.values).shape)
    data_array = np.rollaxis(np.array(data.array.to_list()), 1, 3)
    label_array = np.array(data.Label.to_list())
    np.save('class_data', data_array)
    np.save('class_label', label_array)
     
