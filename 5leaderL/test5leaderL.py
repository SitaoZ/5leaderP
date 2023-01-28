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
    parser = argparse.ArgumentParser(description='PyTorch Implementation of TSAR Predict')

    parser.add_argument('--test_data_path', type=str,
                        help='test data saved in numpy ndarray')
    parser.add_argument('--test_label_path', type=str,
                        help='test label saved in numpy ndarray')
    parser.add_argument('--output', type=str, help='output path')
    return parser.parse_args()


Models = {
    'cnn': RegCnnNet(256, 128),
    'gru': RegGruNet(256, 128),
    'attention':RegAttenNet(),
    'resnet': RegResNet(128, 64),
    'lstm': RegLstmNet(256, 128)
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

def load_dataset(data_path, label_path):
    X = np.load(data_path)
    y = np.load(label_path)
    return X,y

def load_model():
    model_path = ['attention_5.pt','cnn_3.pt','gru_1.pt','lstm_2.pt','resnet_4.pt']
    ensemble = []
    for path in model_path:
        name = path.split('_')[0]
        model = Models[name]
        if torch.cuda.is_available():
            model.cuda()
        model.load_state_dict(torch.load(path))
        ensemble.append(model)
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
    test_data = X_test
    # test DataLoader
    test_set = dataset(test_data, test_label, train=True)
    test_dataloader = DataLoader(dataset=test_set,
                                  batch_size=24,
                                  shuffle=False,
                                  num_workers=2)
    criterion = nn.L1Loss()
    for data, label in test_dataloader:
        with torch.no_grad():
            if torch.cuda.is_available():
                data, label = data.cuda(), label.cuda()
            # forward
            target = model.forward(data)
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
    # print('labels =', labels.reshape(-1,))
    labels = scaler.inverse_transform(labels).reshape(-1,)
    y_test = y_test.reshape(-1,)
    return predictions

# make predictions with the ensemble and calculate a prediction interval
def predict_with_pi(ensemble, X_test, y_test):
    # make predictions
    scaler = load('scaler.joblib')
    yhat = [predict(model, X_test, y_test, scaler) for model in ensemble]
    yhat = asarray(yhat)
    yhat = yhat.transpose()
    # calculate 95% gaussian prediction interval
    interval = 1.96 * yhat.std(axis=1)
    lower, upper = yhat.mean(axis=1) - interval, yhat.mean(axis=1) + interval
    return lower, yhat.mean(axis=1), upper
 
def main():
    # seed
    seed_torch(12)
    # conf
    config = parse_args()
    print(config)
    # step1
    # load dataset
    data_path = config.test_data_path  # '../../another_512/regress_data_peak.npy'
    label_path = config.test_label_path #'../../another_512/regress_label_peak.npy'
    X_test, y_test = load_dataset(data_path, label_path)
    # fit ensemble
    ensemble = load_model()
    # make predictions with prediction interval
    lower, mean, upper = predict_with_pi(ensemble, X_test, y_test)
    df = pd.DataFrame({'lower': lower, 'prediction': mean, 'upper': upper, 'true': y_test.reshape(-1,)})
    df.to_csv(config.output, index=False)
    print('Point prediction: %.3f' % mean[0])
    print('95%% prediction interval: [%.3f, %.3f]' % (lower[0], upper[0]))
    print('True value: %.3f' % y_test[0])
if __name__ == '__main__':
    main()
