#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: predict.py
date: 2022/3/26 4:49 PM
author: Sitao Zhu
mail: zhusitao1990@163.com
'''

import os
import torch
import random
import argparse
import numpy as np
import pandas as pd
from aTSS.models import GruNet, LogisticRegression
from aTSS.models import CnnNet, LstmNet, AttenNet, ResNet
from sklearn.metrics import accuracy_score

Models = {
    'cnn': CnnNet(256, 128),
    'lr': LogisticRegression(),
    'gru': GruNet(256, 128),
    'lstm': LstmNet(256, 128),
    'attention':AttenNet(),
    'resnet': ResNet()
}

def parse_args():
    parser = argparse.ArgumentParser(description='PyTorch Implementation of aTSS Predict')

    parser.add_argument('--model', type=str, help='model name',
                        choices=['lr','cnn','gru','lstm','resnet','attention'])
    parser.add_argument('--predict_data_path', type=str,
                        default='csv for predict',
                        help='contain two columns (seq,label) separated by comma')
    parser.add_argument('--model_dict_path', type=str, help='model saved name')
    parser.add_argument('--output_path', type=str, help='output path')
    return parser.parse_args()


def seed_torch(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed) # if you are using multi-GPU.
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def oneHot(stringInput):
    matrix = np.zeros((4, len(stringInput)))
    seq = stringInput.upper()
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


def predict(config):
    seed_torch(seed=12)
    # data
    df = pd.read_csv(config.predict_data_path)
    df.loc[:,'onehot'] = df.Seq.apply(lambda x: oneHot(x))
    # model
    model = Models[config.model]
    model.load_state_dict(torch.load(config.model_dict_path, map_location ='cpu'))
    # result
    Predict = []
    Probabs = []
    model.eval()
    with torch.no_grad():
        for idx in range(df.shape[0]):
            data = torch.Tensor(df['onehot'][idx])
            data = torch.unsqueeze(data, 0)
            target = model(data).squeeze(1)
            prob = torch.sigmoid(target)
            pred = target.gt(0.5).float()
            label = pred.numpy()[0]
            prob = prob.numpy()[0]
            p = str(round(prob, 4))
            Probabs.append(p)
            if label > 0.5:
                Predict.append(1)
            else:
                Predict.append(0)
    df.loc[:, 'Predict'] = Predict
    df.loc[:, 'Probabs'] = Probabs

    print(accuracy_score(df.Label, df.Predict))
    df[['Predict','Label','Seq',]].to_csv(config.output_path, index=False)

def main():
    config = parse_args()
    predict(config)


if __name__ == '__main__':
    main()
