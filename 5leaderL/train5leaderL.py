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
from aTSS.models import RegResNet, RegLstmNet, RegResAttenNet
# sklearn
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import QuantileTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def parse_args():
    parser = argparse.ArgumentParser(description='PyTorch Implementation of aTSS Predict')
    parser.add_argument('--model', type=str, help='model name',
                        choices=['attention', 'cnn','gru','lstm','resnet'],
                        nargs='+',
                        default=['cnn', 'gru', 'lstm', 'resnet'])
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
    parser.add_argument('--weight_decay', default=1e-5, type=float,
                        help='weight decay L2 regularization (default: 1e-5)')
    parser.add_argument('--model_saved_suffix', type=str, help='model saved suffix (default: None)')
    return parser.parse_args()



Models = {
    'cnn': RegCnnNet(128, 64),
    'gru': RegGruNet(256, 128),
    'attention': RegResAttenNet(128,64),
    'resnet': RegResNet(128, 64),
    'lstm': RegLstmNet(256, 64)
}

"""
Models = {
    'cnn': RegResNet(128, 32),
    'gru': RegResNet(256, 128),
    'attention':RegResNet(256,32),
    'resnet': RegResNet(128, 64),
    'lstm': RegResNet(256, 64)
}
"""

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
        #torch.nn.init.xavier_uniform_(m.weight)
        torch.nn.init.kaiming_uniform_(m.weight, a=0, mode='fan_in', nonlinearity='leaky_relu')
        if m.bias is not None:
            torch.nn.init.constant_(m.bias, 0.0)

    elif isinstance(m,(nn.BatchNorm1d,nn.BatchNorm2d)):
        # torch.nn.init.normal_(m.weight)
        torch.nn.init.constant_(m.weight, 1.0)
        if m.bias is not None:
            torch.nn.init.constant_(m.bias, 0.0)
    elif isinstance(m,(nn.Linear)):
        # t.nn.init.xavier_normal_(m.weight)
        torch.nn.init.xavier_uniform_(m.weight)
        if m.bias is not None:
            torch.nn.init.constant_(m.bias, 0.0)

class EarlyStopping(object):
    """ Early stops training loop if validation loss or accuracy doesn't improve after a given patience. """
    def __init__(self, save_path='saved_model.h5', patience=7, verbose=False, delta=0):
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

class RMSELoss(nn.Module):
    def __init__(self, eps=1e-6):
        super().__init__()
        self.mse = nn.MSELoss()
        self.eps = eps
        
    def forward(self,yhat,y):
        loss = torch.sqrt(self.mse(yhat,y) + self.eps)
        return loss

class RMSLELoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.mse = nn.MSELoss()
        
    def forward(self, pred, actual):
        return torch.sqrt(self.mse(torch.log(pred + 1), torch.log(actual + 1)))

def load_dataset(data_path, label_path):
    X = np.load(data_path)
    y = np.load(label_path)
    y = y.reshape(-1,1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.9, random_state=1)
    # save test 
    np.save('test_data', X_test)
    np.save('test_label', y_test)
    return X_train, X_test, y_train, y_test
    #data = pd.read_csv('regress_peak.csv')
    #data_train, data_test = train_test_split(data, train_size=0.8, random_state=1)
    #data_test.to_csv('data_test.csv', index=False)
    #data_train.loc[:, 'array'] = data_train.Seq.apply(seq2matrix)
    #data_test.loc[:, 'array'] = data_test.Seq.apply(seq2matrix)
    # train
    #X_train = np.rollaxis(np.array(data_train.array.to_list()), 1, 3)
    #y_train = np.array(data_train.Label.to_list())
    # test
    #X_test = np.rollaxis(np.array(data_test.array.to_list()), 1, 3) 
    #y_test = np.array(data_test.Label.to_list())
    #return X_train, X_test, y_train, y_test

def l1_penalty(params, l1_lambda=0.001):
    """Returns the L1 penalty of the params."""
    l1_norm = sum(p.abs().sum() for p in params)
    return l1_lambda*l1_norm

def fit_model(config, model_id, model_index, X_train, y_train, X_val, y_val):
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
    # criterion = nn.SmoothL1Loss()
    # criterion = nn.MSELoss()
    # criterion = RMSLELoss()
    # criterion = RMSELoss()
    criterion = nn.L1Loss()
    # optimizer = torch.optim.RMSprop(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.lr, betas=(0.9, 0.999), weight_decay=config.weight_decay)
    # optimizer = torch.optim.SGD(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)
    # learning rate decay
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=config.lr_decay,
                                                verbose=True)
    #scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[20, 40, 60, 80, 120, 160, 200], gamma=0.6, verbose=True)
    # step5 data split
    train_data= X_train
    train_label = y_train
    # scale
    # scaler = MinMaxScaler()
    scaler = StandardScaler()
    # scaler = QuantileTransformer()
    train_label = train_label.reshape(-1, 1)
    # one step 
    # train_label = scaler.fit_transform(train_label).reshape(-1, )
    scaler.fit(train_label)
    train_label = scaler.transform(train_label).reshape(-1, )
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
            # L1 regularization
            # loss = loss + l1_penalty(model.parameters())
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
        # valid in epoch loop
        yhat, val_loss = validate(model, X_val, y_val, scaler)
        y_val = y_val.reshape(-1,)
        val_mae = mean_absolute_error(y_val, yhat)
        # early_stopping(train_loss_epoch, model)
        early_stopping(val_loss, model)
        if early_stopping.early_stop:
            print(f"Early stopping at epoch {e}")
            torch.save(model.state_dict(), f'{model_id}.pt')
            break
    torch.save(model.state_dict(), f'{model_id}.pt')
    return model, scaler
 


# fit an ensemble of models
def fit_ensemble(config, model_list, X_train, y_train, X_val, y_val):
    ensemble = list()
    for i, model_id in enumerate(model_list, start=1):
        # define and fit the model on the training set
        model, scaler = fit_model(config, model_id, i, X_train, y_train, X_val, y_val)
        # evaluate model on the test set
        # model.load_state_dict(torch.load(f'{model_id}.pt'))
        # valiade in each model 
        yhat = predict(model, X_val, y_val, scaler)
        y_val = y_val.reshape(-1,)
        df = pd.DataFrame({'predict': yhat, 'label': y_val})
        df.to_csv(f'{model_id}_{i}_predict2_result.csv', index=False)
        mae = mean_absolute_error(y_val, yhat)
        print('>%d, Validation MAE: %.3f' % (i, mae))
        # store the model
        ensemble.append((model, scaler))
    return ensemble
 
def validate(model ,X_val, y_val, scaler):
    # validate model
    correct = 0
    val_loss = 0.0
    predictions = np.array([])
    labels = np.array([])
    seqs = np.array([])
    val_label = y_val.reshape(-1, 1)
    val_label = scaler.transform(val_label).reshape(-1, )
    val_data = X_val
    # val DataLoader
    val_set = dataset(val_data, val_label, train=True)
    val_dataloader = DataLoader(dataset=val_set,
                                  batch_size=24,
                                  # shuffle=True,
                                  shuffle=False,
                                  num_workers=2)
    # criterion = nn.SmoothL1Loss()
    # criterion = nn.MSELoss()
    # criterion = RMSLELoss()
    # criterion = RMSELoss()
    criterion = nn.L1Loss()
    model.eval()
    for data, label in val_dataloader:
        with torch.no_grad():
            if torch.cuda.is_available():
                data, label = data.cuda(), label.cuda()
            # forward
            target = model(data)
            target = target.squeeze(1)
            # loss cal
            loss = criterion(target, label)
            # val loss cal
            val_loss += loss.item() * data.size(0)
            predictions = np.append(predictions, target.cpu())
            labels = np.append(labels, label.cpu())
            seqs = np.append(seqs, matrix2seq(data.cpu()))
    val_loss_average = val_loss / len(val_dataloader.dataset)
    # inverse transform
    predictions = predictions.reshape(-1,1)
    predictions = scaler.inverse_transform(predictions).reshape(-1,)
    labels = labels.reshape(-1, 1)
    labels = scaler.inverse_transform(labels).reshape(-1,)
    # cal
    MAE = train_utils.rmse(predictions, labels)
    MSE = train_utils.mse(predictions, labels)
    R2 = train_utils.r_square(predictions, labels)
    print(f"MAE = {MAE}, R2={R2}")
    return predictions, val_loss_average


def predict(model ,X_test, y_test, scaler):
    # validate model
    correct = 0
    test_loss = 0.0
    predictions = np.array([])
    labels = np.array([])
    seqs = np.array([])
    test_label = y_test.reshape(-1, 1)
    test_label = scaler.transform(test_label).reshape(-1, )
    test_data = X_test
    # test DataLoader
    test_set = dataset(test_data, test_label, train=True)
    test_dataloader = DataLoader(dataset=test_set,
                                  batch_size=24,
                                  shuffle=False,
                                  num_workers=2)
    # criterion = nn.SmoothL1Loss()
    # criterion = nn.MSELoss()
    # criterion = RMSLELoss()
    # criterion = RMSELoss()
    criterion = nn.L1Loss()
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
    labels = scaler.inverse_transform(labels).reshape(-1,)
    # out
    df = pd.DataFrame({'Predict': predictions, 'Label': labels, 'Raw_label': y_test.reshape(-1,), 'Seqs': seqs})
    model_name = model.model_name()
    df.to_csv(f'{model_name}_predict_result.csv', index=False)

    MAE = train_utils.rmse(predictions, labels)
    MSE = train_utils.mse(predictions, labels)
    R2 = train_utils.r_square(predictions, labels)
    print(f"MAE = {MAE}, R2={R2}")
    return predictions

# make predictions with the ensemble and calculate a prediction interval
def predict_with_pi(ensemble, X_test, y_test):
    # make predictions
    yhat = [predict(model, X_test, y_test, scaler) for (model,scaler) in ensemble]
    print('yhat',yhat)
    yhat = asarray(yhat)
    print('yhat.shape',yhat.shape)
    yhat = yhat.transpose()
    # calculate 95% gaussian prediction interval
    interval = 1.96 * yhat.std(axis=1)
    lower, upper = yhat.mean(axis=1) - interval, yhat.mean(axis=1) + interval
    lower = np.clip(lower,0,256)
    upper = np.clip(upper,0,256)
    predict_value = yhat.mean(axis=1)
    predict_value = np.clip(predict_value,0,256)
    return lower, predict_value, upper
 
def main():
    # seed
    seed_torch(1)
    # configure
    config = parse_args()
    print(config)
    # step1 load dataset
    data_path = config.train_data_path   # regress_data_peak.npy
    label_path = config.train_label_path # regress_label_peak.npy
    trainData, X_test, trainLabel, y_test = load_dataset(data_path, label_path)
    print(trainData.shape)
    # step 2 fit ensemble train and validate
    kfold = KFold(n_splits=10, shuffle=True)
    for fold, (train_index, valid_index) in enumerate(kfold.split(trainData)):
        model_list = config.model
        print(f'{fold} model_list', model_list)
        # kfold split
        X_train, X_val = trainData[train_index], trainData[valid_index]
        y_train, y_val = trainLabel[train_index], trainLabel[valid_index]
        ensemble = fit_ensemble(config, model_list, X_train, y_train, X_val, y_val)
        # step 3 make predictions with prediction interval
        lower, mean, upper = predict_with_pi(ensemble, X_test, y_test)
        print('lower =', lower.shape)
        print('lower =', lower)
        df = pd.DataFrame({'lower': lower, 'prediction': mean, 'upper': upper, 'true': y_test.reshape(-1,)})
        test_mae = train_utils.rmse(df.prediction, df.true)
        print(f"Fold-{fold} test MAE=", test_mae)
        df.to_csv(f'prediction_interval_fold{fold}.csv', index=False)
        print('Point prediction: %.3f' % mean[0])
        print('95%% prediction interval: [%.3f, %.3f]' % (lower[0], upper[0]))
        print('True value: %.3f' % y_test[0])
        break
if __name__ == '__main__':
    main()
