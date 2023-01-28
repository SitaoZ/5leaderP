#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: dataset.py
date: 2021/12/26 上午11:05
author: Sitao Zhu
mail: zhusitao1990@163.com
'''


import torch
import numpy as np
from torch.utils.data import Dataset


class dataset(Dataset):
    """
    process dataframe
    """
    def __init__(self, data_array, label_array, train=True):
        super(dataset, self).__init__()
        self.data_ndarray = data_array
        self.label_ndarray = label_array
        self.train = train
        self.data, self.label = self.preprocess()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        data = self.data[index]
        label = self.label[index]
        return data, label

    def preprocess(self):

        data = self.data_ndarray
        data = np.transpose(data, (0, 2, 1))  # [N, L , C] --> [N, C, L] CNN
        label = self.label_ndarray
        if self.train:
            # unique for train, not for test
            data, indices = np.unique(data, axis=0, return_index=True)
            data = torch.from_numpy(data).float()
            # corresponding to data indices
            label = label[indices]
            label = torch.from_numpy(label).float()
            return data, label
        else:
            data = torch.from_numpy(data).float()
            label = torch.from_numpy(label).float()
            return data, label
