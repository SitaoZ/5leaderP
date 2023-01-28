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

    parser.add_argument('--train_data_path', type=str,
                        default='train_class_data.npy',
                        help='train data saved in numpy ndarray')
    parser.add_argument('--train_label_path', type=str,
                        default='train_class_label.npy',
                        help='train label saved in numpy ndarray')
    parser.add_argument('--batch_size', type=int,
                        default=64,
                        help='train batch size(default: 64)')
    parser.add_argument('--epoch', type=int,
                        default=10,
                        help='train epoch(default: 10)')

    parser.add_argument('--lr', default=0.001, type=float,
                        help='learning rate (default: 0.001)')
    parser.add_argument('--lr_decay', default=0.95, type=float,
                        help='learning rate decay (default: 0.95)')

    parser.add_argument('--model_saved', type=str, help='model saved name')
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


def seed_torch(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed) # if you are using multi-GPU.
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

def init_weights(m):
    """
    pytorch model parameters initiation
    :param m:
    :return:
    """
    if isinstance(m,(nn.Conv1d,nn.Conv2d)):
        torch.nn.init.xavier_uniform_(m.weight)
        if m.bias is not None:
            torch.nn.init.constant_(m.bias, 0.0)

    elif isinstance(m,(nn.BatchNorm1d,nn.BatchNorm2d)):
        torch.nn.init.normal_(m.weight)
        if m.bias is not None:
            torch.nn.init.constant_(m.bias, 0.0)
    elif isinstance(m,(nn.Linear)):
        # t.nn.init.xavier_normal_(m.weight)
        torch.nn.init.xavier_uniform_(m.weight)
        # torch.nn.init.constant_(m.bias, 0.0)

class EarlyStopping(object):
    """ Early stops training loop if validation loss or accuracy doesn't improve after a given patience. """
    def __init__(self, save_path='saved_model.h5', patience=10, verbose=False, delta=0):
        self.save_path = save_path
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loos_min = np.Inf
        self.delta = delta

    def __call__(self, val_loss, model):
        """ a built-in function enables programmers to write classes where the instances
        behave like functions and can be called like a function"""
        score = -val_loss
        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)

        elif score < self.best_score + self.delta:
            self.counter += 1
            print(f'EarlyStopping counter:{self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        ''' Saves model when validation loss decrease'''
        if self.verbose:
            print(f'Validation loss decreased ({self.val_loos_min:.6f} --> {val_loss:.6f}). Saving model ...')
        torch.save(model.state_dict(), self.save_path)
        self.val_loos_min = val_loss


def load_dataset(data_path, label_path):
    X = np.load(data_path)
    y = np.load(label_path)
    y = y.reshape(-1,1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.9, random_state=1)
    # scale input data
    #scaler = MinMaxScaler()
    #scaler.fit(y_train)
    #y_train = scaler.transform(y_train)
    #y_test = scaler.transform(y_test)
    return X_train, X_test, y_train, y_test

def fit_model(config, model_id, model_index, X_train, y_train):
    # step1 data
    # step 2 Satisfaction Index
    max_mae = np.inf
    max_mse = np.inf
    cost_total = []
    # step3 model instance
    model = Models[model_id]
    print(model)
    model.apply(init_weights)
    if torch.cuda.is_available():
        model.cuda()
    # step4 loss function and optimizer
    criterion = nn.MSELoss()
    # criterion = RMSELoss()
    # criterion = nn.L1Loss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.lr, betas=(0.9, 0.999), weight_decay=1e-5)
    # learning rate decay
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.7,
                                                verbose=True)
    #scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[20, 40, 60, 80, 120, 160, 200], gamma=0.6, verbose=True)
    # step5 data split
    train_data= X_train
    train_label = y_train
    # scale
    scaler = MinMaxScaler()
    # scaler = StandardScaler()
    train_label = train_label.reshape(-1, 1)
    train_label = scaler.fit_transform(train_label).reshape(-1, )
    # scaler to save
    dump(scaler, 'scaler.joblib')
    # train DataLoader
    train_set = dataset(train_data, train_label, train=True)
    train_dataloader = DataLoader(dataset=train_set,
                                  batch_size=config.batch_size,
                                  shuffle=True,
                                  num_workers=2)
    # early stop avoid overfitting 
    early_stopping = EarlyStopping()
    for e in range(config.epoch):
        train_loss_epoch = 0.0
        model.train()
        for batch_idx, (data, label) in enumerate(train_dataloader):
            if torch.cuda.is_available():
                data, label = data.cuda(), label.cuda()
            # grad clear
            optimizer.zero_grad()
            # forward
            target = model(data)
            target = target.squeeze(1) # to one dimention
            # loss cal
            loss = criterion(target, label)
            loss.backward()
            # parameter update
            optimizer.step()
            # cumulate loss
            train_loss = loss.item() * data.size(0) # batch cumulative loss
            train_loss_epoch += train_loss
            if batch_idx % 10 == 0:
                print(f'{time.strftime("%y%m%d_%H:%M:%S")} train epoch {e+1} '
                      f'[{batch_idx}/{len(train_dataloader)}] '
                      f'({100*batch_idx/len(train_dataloader):.0f}%)\t'
                      f'{train_loss:.6f}')
        train_loss_epoch = train_loss_epoch/len(train_dataloader)
        cost_total.append(train_loss_epoch)
        print('train loss: '
              f'{time.strftime("%y%m%d_%H:%M:%S")} train epoch {e+1} '
              f'{train_loss_epoch:.6f}')   
        scheduler.step() # learning rate decay
        early_stopping(train_loss_epoch, model)
        if early_stopping.early_stop:
            print(f"Early stopping at epoch {e}")
            torch.save(model.state_dict(), f'{model_id}.pt')
            break
    torch.save(model.state_dict(), f'{model_id}.pt')
    return model, scaler
 


# fit an ensemble of models
def fit_ensemble(config, n_members, X_train, X_test, y_train, y_test):
    ensemble = list()
    # model_id = 'gru'
    model_list = ['attention','resnet_1', 'resnet_2', 'resnet_3', 'cnn_3', 'cnn_4', 'gru_5', 'gru_6',  'lstm_7', 'lstm_8']
    # model_list = ['resnet_1','resnet_2','cnn_3','cnn_4','gru_5','gru_6','lstm_7','lstm_8','gru_9','gru_10']

    # model_list = ['attention']*3
    for i,model_id in zip(range(n_members),model_list):
        # define and fit the model on the training set
        model, scaler = fit_model(config, model_id, i+1, X_train, y_train)
        # evaluate model on the test set
        # model.load_state_dict(torch.load(f'{model_id}.pt'))
        yhat = predict(model, X_test, y_test, scaler)
        y_test = y_test.reshape(-1,)
        df = pd.DataFrame({'predict': yhat, 'label': y_test})
        df.to_csv(f'{model_id}_{i+1}_predict2_result.csv', index=False)
        print('yhat =', yhat.shape)
        print('y_test =', y_test.shape)
        mae = mean_absolute_error(y_test, yhat)
        print('>%d, MAE: %.3f' % (i+1, mae))
        # store the model
        ensemble.append((model, scaler))
    return ensemble
 

def predict(model ,X_test, y_test, scaler):
    # validate model
    correct = 0
    test_loss = 0.0
    predictions = np.array([])
    labels = np.array([])
    seqs = np.array([])
    test_label = y_test.reshape(-1, 1)
    test_label = scaler.transform(test_label).reshape(-1, )
    print('test_label =', test_label)
    test_data = X_test
    print('test_data =', test_data.shape)
    # test DataLoader
    test_set = dataset(test_data, test_label, train=True)
    test_dataloader = DataLoader(dataset=test_set,
                                  batch_size=24,
                                  # shuffle=True,
                                  shuffle=False,
                                  num_workers=2)
    print('test_dataloader =', len(test_dataloader.dataset))
    # criterion = nn.L1Loss()
    criterion = nn.MSELoss()
    model.eval()
    for data, label in test_dataloader:
        with torch.no_grad():
            if torch.cuda.is_available():
                data, label = data.cuda(), label.cuda()
            # forward
            target = model(data)
            target = target.squeeze(1)
            # loss cal
            loss = criterion(target, label)
            # test loss cal
            test_loss += loss.item() * data.size(0)
            predictions = np.append(predictions, target.cpu())
            labels = np.append(labels, label.cpu())
            seqs = np.append(seqs, matrix2seq(data.cpu()))
    test_loss_average = test_loss / len(test_dataloader.dataset)
    # inverse transform
    predictions = predictions.reshape(-1,1)
    predictions = scaler.inverse_transform(predictions).reshape(-1,)
    labels = labels.reshape(-1, 1)
    print('labels =', labels.reshape(-1,))
    labels = scaler.inverse_transform(labels).reshape(-1,)
    df = pd.DataFrame({'Predict': predictions, 'Label': labels, 'Raw_label': y_test.reshape(-1,), 'Seqs': seqs})
    model_name = model.model_name()
    df.to_csv(f'{model_name}_predict_result.csv', index=False)

    MAE = train_utils.rmse(predictions, labels)
    MSE = train_utils.mse(predictions, labels)
    R2 = train_utils.r_square(predictions, labels)
    print("MAE =", MAE)
    return predictions

# make predictions with the ensemble and calculate a prediction interval
def predict_with_pi(ensemble, X_test, y_test):
    # make predictions
    yhat = [predict(model, X_test, y_test, scaler) for (model,scaler) in ensemble]
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
    # step1 training
    # load dataset
    data_path = config.train_data_path  # '../../another_512/regress_data_peak.npy'
    label_path = config.train_label_path #'../../another_512/regress_label_peak.npy'
    X_train, X_test, y_train, y_test = load_dataset(data_path, label_path)
    # fit ensemble
    n_members = 10
    ensemble = fit_ensemble(config, n_members, X_train, X_test, y_train, y_test)
    # make predictions with prediction interval
    lower, mean, upper = predict_with_pi(ensemble, X_test, y_test)
    print('lower =', lower.shape)
    print('lower =', lower)
    df = pd.DataFrame({'lower': lower, 'prediction': mean, 'upper': upper, 'true': y_test.reshape(-1,)})
    df.to_csv('prediction_interval.csv', index=False)
    print('Point prediction: %.3f' % mean[0])
    print('95%% prediction interval: [%.3f, %.3f]' % (lower[0], upper[0]))
    print('True value: %.3f' % y_test[0])

if __name__ == '__main__':
    main()
