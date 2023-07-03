#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: main.py
date: 2021/12/26 上午10:53
author: Sitao Zhu
mail: zhusitao1990@163.com
'''
import os
import time
import pickle
import argparse
import torch
import numpy as np
from torch import nn
from aTSS import train_utils
from joblib import load, dump
from aTSS.dataset import dataset
from aTSS.models import RegGruNet,RegCnnNet,RegLstmNet,RegResNet
from torch.utils.data import DataLoader
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from ray import tune
from ray.tune import CLIReporter
from ray.tune.schedulers import ASHAScheduler


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
                        help='train batch size')
    parser.add_argument('--epoch', type=int,
                        default=10,
                        help='train epoch')

    parser.add_argument('--test_data_path', type=str,
                        default='test_class_data.npy',
                        help='test data saved in numpy ndarry')
    parser.add_argument('--test_label_path', type=str,
                        default='test_class_label.npy',
                        help='test label saved in numpy ndarray')

    parser.add_argument('--lr', '-l', default=0.001, type=float,
                        help='learning rate (default: 0.001)')
    parser.add_argument('--lr_decay','-d', default=0.95, type=float,
                        help='learning rate decay (default: 0.95)')

    parser.add_argument('--model_name', type=str, help='model saved name')
    return parser.parse_args()

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
        torch.nn.init.constant_(m.bias, 0.0)

def train(config, checkpoint_dir = None, epochs=5):
    """
    Train model and validate in every epoch
    :param train_dataloader:
    :param valid_dataloader:
    :param model:
    :param criterion:
    :param optimizer:
    :param epochs:
    :return:
    """
    # step1 data
    train_data = np.load('/home/zhusitao/AI/TSS_Predict/ath/final_version/regress/github/data/random_select/regress_data_peak.npy')
    train_label = np.load('/home/zhusitao/AI/TSS_Predict/ath/final_version/regress/github/data/random_select/regress_label_peak.npy')
    train_label = train_label.reshape(-1, 1)
    print('train_label shape:', train_label.shape)
    X_train, X_test, y_train, y_test = train_test_split(train_data, train_label, train_size=0.8, random_state=1)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, train_size=0.75, random_state=1)
    y_val = y_val.reshape(-1, )

    # scaler = StandardScaler()
    scaler = MinMaxScaler()
    y_train = y_train.reshape(-1, 1)
    scaler.fit(y_train)
    y_train = scaler.transform(y_train).reshape(-1, )
    # scaler to save
    dump(scaler, 'scaler.joblib')

    train_set = dataset(X_train, y_train, train=True)

    # to dataloader; train spilt a validation set
    valid_set = dataset(X_val, y_val, train=False)


    # train set
    train_dataloader = DataLoader(dataset=train_set,
                                  batch_size=config['batch_size'],
                                  shuffle=True,
                                  num_workers=2)
    # valid set
    valid_dataloader = DataLoader(dataset=valid_set,
                                  batch_size=24,
                                  shuffle=False,
                                  num_workers=2)


    # step2 model
    # model = RegGruNet(config['l1'], config['l2'])
    model = RegCnnNet(config['l1'], config['l2'])
    # model = RegLstmNet(config['l1'], config['l2'])
    # model = RegResNet(config['l1'], config['l2'])
    model.apply(init_weights)
    if torch.cuda.is_available():
        model.cuda()

    # step3 loss function and optimizer
    # criterion = nn.MSELoss()
    criterion = nn.SmoothL1Loss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config['lr'])

    if checkpoint_dir:
        model_state = torch.load(os.path.join(checkpoint_dir, "checkpoint"))
        model.load_state_dict(model_state)

    # setp4 train
    max_mae = np.inf
    for e in range(10):
        train_loss = 0.0
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
            if batch_idx % 10 == 0:
                print(f'{time.strftime("%y%m%d_%H:%M:%S")} train epoch {e+1} '
                      f'[{batch_idx}/{len(train_dataloader)}] '
                      f'({100*batch_idx/len(train_dataloader):.0f}%)\t'
                      f'{train_loss:.6f}')
        # step5 valid
        valid_loss, MAE = valid(valid_dataloader, model, criterion, scaler)
        # if max_mae > MAE:
        #     print(f'MAE Decreased({max_mae:.6f}--->{MAE:.6f}) \t Saving The Model')
        #     max_mae = MAE
        #     torch.save(model.state_dict(), 'regression.h5')
        # 保存检查点
        # ray.tune.checkpoint_dir(step)返回检查点路径
        with tune.checkpoint_dir(e) as checkpoint_dir:
            path = os.path.join(checkpoint_dir, "checkpoint")
            torch.save((model.state_dict(), optimizer.state_dict()), path)
        # 打印平均损失和平均精度
        tune.report(loss=valid_loss, MAE=MAE)



def valid(valid_dataloader, model, criterion, scaler):
    """
    Validate the training model in every epoch
    :param valid_dataloader:
    :param model:
    :param criterion:
    :return:
    """
    # validate model
    correct = 0
    valid_loss = 0.0
    predictions = np.array([])
    labels = np.array([])
    model.eval()
    for data, label in valid_dataloader:
        with torch.no_grad():
            if torch.cuda.is_available():
                data, label = data.cuda(), label.cuda()
            # forward
            target = model(data)
            target = target.squeeze(1)
            # loss cal
            loss = criterion(target, label)
            # valid loss cal
            valid_loss += loss.item() * data.size(0)
            predictions = np.append(predictions, target.cpu())
            labels = np.append(labels, label.cpu())
    predictions = predictions.reshape(-1, 1)
    predictions = scaler.inverse_transform(predictions)
    predictions = predictions.reshape(-1, )
    # labels = labels.reshape(-1, 1)
    # labels = scaler.inverse_transform(labels)
    labels = labels.reshape(-1, )
    # MAE = train_utils.rmse(predictions, labels)
    MAE = mean_absolute_error(predictions, labels)

    return valid_loss/len(valid_dataloader.dataset), MAE


def main():
    args = parse_args()
    print(args)
    # ray tune hyper parameter searching
    # ASHAScheduler会根据指定标准提前中止坏实验
    # ASHAScheduler指定参数和CLIReporter中的一致
    scheduler = ASHAScheduler(
        metric="loss",
        mode="min",
        grace_period=1,
        reduction_factor=2)
    # 在命令行打印实验报告
    reporter = CLIReporter(
        parameter_columns=["l1", "l2", "lr", "batch_size"],
        metric_columns=["loss", "MAE", "training_iteration"])
    # "lr": tune.loguniform(1e-4, 1e-1),
    config = {
        "l1": tune.sample_from(lambda _: 2 ** np.random.randint(5, 8)),
        "l2": tune.sample_from(lambda _: 2 ** np.random.randint(2, 7)),
        "lr": tune.choice([1e-5, 1e-4, 1e-3, 1e-2]),
        "batch_size": tune.choice([24, 32, 48, 64, 128])
    }
    # 执行训练过程
    result = tune.run(
        train,
        config=config,
        num_samples=50,
        resources_per_trial={"cpu": 8, "gpu": 1},
        scheduler=scheduler,
        progress_reporter=reporter)

    # 找出最佳实验
    # best_trial = result.get_best_trial("loss", "min", "last")
    best_trial = result.get_best_trial("MAE", "min", "last")
    # 打印最佳实验的参数配置
    print("Best trial config: {}".format(best_trial.config))
    # 打印最终的验证集的的损失
    print("Best trial final validation loss: {}".format(
        best_trial.last_result["loss"]))
    # 打印最终的验证集的准确性
    print("Best trial final validation MAE: {}".format(
        best_trial.last_result["MAE"]))



if __name__ == '__main__':
    main()
