#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: train_r.py
date: 2021/3/3 2:56 PM
author: Sitao Zhu
mail: zhusitao1990@163.com
'''

# torch
import os
import time
import torch
import random
import argparse
from torch import nn
from torch.utils.data import DataLoader
# numpy 
import numpy as np
import pandas as pd
from numpy import  asarray
from joblib import load, dump
# model
from aTSS import train_utils
from aTSS.dataset import dataset
from aTSS.preprocessing import matrix2seq, shuffle_arrays
from aTSS.models import RegCnnNet, RegGruNet, RegAttenNet
from aTSS.models import RegResNet, RegLstmNet
# sklearn
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def parse_args():
    parser = argparse.ArgumentParser(description='PyTorch Implementation of aTSS Predict')

    parser.add_argument('--predict_data_path', type=str,
                        help='predict data saved in csv')
    parser.add_argument('--output', type=str, help='output path')
    return parser.parse_args()




Models = {
    'resnet_1': RegResNet(128, 64),
    'resnet_2': RegResNet(64, 32),
    'resnet_3': RegResNet(100, 32),
    'resnet_4': RegResNet(64, 16),
    'resnet_5': RegResNet(100, 16),
    'cnn_3': RegCnnNet(256, 128),
    'cnn_4': RegCnnNet(256, 64),
    'gru_5': RegGruNet(256, 128),
    'gru_6': RegGruNet(256, 64),
    'lstm_7': RegLstmNet(256, 128),
    'lstm_8': RegLstmNet(256, 64),
    'gru_9': RegGruNet(128, 64),
    'gru_10': RegGruNet(100, 64),
    'attention':RegAttenNet(),
}

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

def seed_torch(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed) # if you are using multi-GPU.
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

def load_dataset(data_path):
    X = pd.read_csv(data_path)
    X.loc[:,'onehot'] = X.Seq.apply(oneHot)
    array =  np.array(X['onehot'].to_list())
    array = np.rollaxis(array, 1, 3)
    return array

def load_model():
    model_path = ['resnet_1', 'resnet_2', 'resnet_3', 'cnn_3', 'cnn_4', 'gru_5', 'gru_6',  'lstm_7', 'lstm_8']
    ensemble = []
    for path in model_path:
        model = Models[path]
        if torch.cuda.is_available():
            model.cuda()
        model_dict = path+'.pt'
        model.load_state_dict(torch.load(model_dict))
        ensemble.append(model)
    return ensemble

def predict(model ,X_test, scaler):
    predictions = np.array([])
    test_data = X_test
    print('test_data =', test_data.shape)
    # test DataLoader
    test_label = np.array([1]*len(test_data))
    test_set = dataset(test_data, test_label, train=False)
    test_dataloader = DataLoader(dataset=test_set,
                                  batch_size=24,
                                  shuffle=False,
                                  num_workers=2)
    print('test_dataloader =', len(test_dataloader.dataset))
    for data, label in test_dataloader:
        with torch.no_grad():
            if torch.cuda.is_available():
                data, label = data.cuda(), label.cuda()
            # forward
            target = model.forward(data)
            target = target.squeeze(1)
            predictions = np.append(predictions, target.cpu())
    predictions = predictions.reshape(-1,1)
    predictions = scaler.inverse_transform(predictions).reshape(-1,)
    print('predictions=',predictions.shape)
    return predictions

# make predictions with the ensemble and calculate a prediction interval
def predict_with_pi(ensemble, X_test):
    # make predictions
    scaler = load('scaler.joblib')
    yhat = [predict(model, X_test, scaler) for model in ensemble]
    yhat = asarray(yhat)
    yhat = yhat.transpose()
    # calculate 95% gaussian prediction interval
    interval = 1.96 * yhat.std(axis=1)
    lower, upper = yhat.mean(axis=1) - interval, yhat.mean(axis=1) + interval
    lower = np.clip(lower,1,150)
    upper = np.clip(upper,1,150)
    predict_value = yhat.mean(axis=1)
    predict_value = np.clip(predict_value,1,150)
    return lower, predict_value, upper
 
def main():
    # seed
    seed_torch(12)
    # conf
    config = parse_args()
    print(config)
    # step1
    # load dataset
    data_path = config.predict_data_path
    input_df = pd.read_csv(data_path)
    X_test= load_dataset(data_path)
    # load ensemble
    ensemble = load_model()
    # make predictions with prediction interval
    lower, mean, upper = predict_with_pi(ensemble, X_test)
    print('lower =', lower.shape)
    print('lower =', lower)
    # df = pd.DataFrame({'lower': lower, 'prediction': mean, 'upper': upper})
    df = pd.DataFrame({'Locus': input_df.Locus.to_list(),'Seq':input_df.Seq.to_list(), 'Start':input_df.Start.to_list(), 'End':input_df.End.to_list(), 'Label':input_df.Label.to_list(), 'lower': lower, 'prediction': mean, 'upper': upper})
    df.to_csv(config.output, index=False)
    print('Point prediction: %.3f' % mean[0])
    print('95%% prediction interval: [%.3f, %.3f]' % (lower[0], upper[0]))
if __name__ == '__main__':
    main()
