#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: hyperSearchClass.py
date: 2021/12/28 下午2:28
author: Sitao Zhu
mail: zhusitao1990@163.com
'''

import os
import time
import argparse
import torch
import numpy as np
import pandas as pd
from torch import nn
import seaborn as sns
from aTSS import train_utils
from aTSS.dataset import dataset
import matplotlib.pyplot as plt
from sklearn.metrics import auc
from sklearn.model_selection import KFold
from torch.utils.data import DataLoader
from aTSS.preprocessing import matrix2seq
from aTSS.models import LogisticRegression
plt.rcParams.update({'figure.max_open_warning': 0})


from ray import tune
from ray.tune import CLIReporter
from ray.tune.schedulers import ASHAScheduler

def parse_args():
    parser = argparse.ArgumentParser(description='PyTorch Implementation of aTSS Predict')

    parser.add_argument('--model', type=str, help='model name',
                        choices=['lr','cnn','cnn_gru','cnn_lstm','cnn_attention'])
    parser.add_argument('--train_data_path', type=str,
                        default='train_class_data.npy',
                        help='train data saved in numpy ndarray')
    parser.add_argument('--train_label_path', type=str,
                        default='train_class_label.npy',
                        help='train label saved in numpy ndarray')
    parser.add_argument('--batch_size',default=64, type=int,
                        help='train batch size (default: 64)')
    parser.add_argument('--epoch', default=10, type=int,
                        help='train epoch (default: 10)')
    parser.add_argument('--lr', default=0.001, type=float,
                        help='learning rate (default: 0.001)')
    parser.add_argument('--lr_decay', default=0.95, type=float,
                        help='learning rate decay (default: 0.95)')

    parser.add_argument('--model_saved', type=str, help='model saved name')
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
        torch.nn.init.xavier_uniform_(m.weight)
        torch.nn.init.constant_(m.bias, 0.0)


def train(config, checkpoint_dir = None):
    """
    model train
    :param config:
    :param checkpoint_dir:
    :return:
    """
    # step1 data
    train_data_array = np.load('../data/class_data.npy')
    train_label_array = np.load('../data/class_label.npy')

    # 加载预训练模型
    if checkpoint_dir:
        model_state = torch.load(os.path.join(checkpoint_dir, "rice.h5"))
        model.load_state_dict(model_state)

    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)
    # Kfold cross validation
    fig, ax = plt.subplots()

    auc_score_kfold = 0
    kfold = KFold(n_splits=10, shuffle=True)
    for fold, (train_index, valid_index) in enumerate(kfold.split(train_data_array)):
        # step 2 Satisfaction Index
        min_valid_loss = np.inf
        max_accuracy = np.NINF
        max_f1_score = np.NINF
        max_auc = np.NINF
        # step 3 model instance
        # model = LogisticRegression()
        model = LogisticRegression()
        model.apply(init_weights)
        if torch.cuda.is_available():
            model.cuda()

        # step 4 loss function and optimizer
        criterion = nn.BCEWithLogitsLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=config['lr'], betas=(0.9, 0.999))
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=30,
                                                    gamma=0.5, verbose=True)  # learning rate decay

        train_data, valid_data = train_data_array[train_index], train_data_array[valid_index]
        train_label, valid_label = train_label_array[train_index], train_label_array[valid_index]

        # train set
        train_set = dataset(train_data, train_label, train=True)
        train_dataloader = DataLoader(dataset=train_set,
                                      batch_size=config['batch_size'],
                                      shuffle=True,
                                      num_workers=2)
        # valid set
        valid_set = dataset(valid_data, valid_label, train=True)
        valid_dataloader = DataLoader(dataset=valid_set,
                                      batch_size=24,
                                      shuffle=True,
                                      num_workers=2)
        for e in range(10):
            train_loss = 0.0
            model.train()  # set flag in Dropout and BatchNorm
            for batch_idx, (data, label) in enumerate(train_dataloader):
                if torch.cuda.is_available():
                    data, label = data.cuda(), label.cuda()
                # grad clear
                # data = data.reshape(-1,4*512)
                optimizer.zero_grad()
                # forward
                target = model(data)
                target = target.squeeze(1)  # to one dimention
                # loss cal
                loss = criterion(target, label)
                loss.backward()
                # parameter update
                optimizer.step()
                # cumulate loss
                train_loss = loss.item() * data.size(0)  # batch cumulative loss
                if batch_idx % 10 == 0:
                    print(f'{fold+1} Fold '
                          f'{time.strftime("%y%m%d_%H:%M:%S")} train epoch {e+1}'
                          f'[{batch_idx}/{len(train_dataloader)}] '
                          f'({100*batch_idx/len(train_dataloader):.0f}%)\t'
                          f'{train_loss:.6f}')
            scheduler.step()  # learning rate decay
            # step5 valid
            valid_loss, accuracy, f1, fpr, tpr, auc_score = valid(valid_dataloader, model, criterion, fold+1)

            # 保存检查点
            # ray.tune.checkpoint_dir(step)返回检查点路径
            with tune.checkpoint_dir(e) as checkpoint_dir:
                path = os.path.join(checkpoint_dir, "checkpoint")
                torch.save((model.state_dict(), optimizer.state_dict()), path)
            # 打印平均损失和平均精度
            tune.report(loss=valid_loss, accuracy=accuracy)

            if e == (10 - 1):
                # last epoch
                interp_tpr = np.interp(mean_fpr, fpr, tpr)
                interp_tpr[0] = 0.0
                aucs.append(auc_score)
                tprs.append(interp_tpr)
                ax.plot(
                    fpr,
                    tpr,
                    color=sns.color_palette("Set2", 10)[fold - 1],
                    label=r"ROC Fold %i (AUC = %0.2f)" % (fold, auc_score),
                    lw=1,
                    alpha=0.8,
                )
                # save model
                torch.save(model.state_dict(), 'saved_model.h5')
    # training finished plot ROC and data
    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    std_tpr = np.std(tprs, axis=0)
    std_auc = np.std(aucs)
    mean_auc = auc(mean_fpr, mean_tpr)
    ax.plot(
        mean_fpr,
        mean_tpr,
        'k--',
        label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
        lw=2,
        alpha=0.8,
    )
    fig.savefig('Mean_ROC.png')
    # fileout
    df_mean = pd.DataFrame(dict(fpr=mean_fpr, tpr=mean_tpr))
    df_mean.to_csv('ROC_Curve_mean_data.csv', index=False)



def valid(valid_dataloader, model, criterion, fold):
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
    seqs = np.array([])

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
            # pred
            pred = torch.sigmoid(target)
            predictions = np.append(predictions, pred.cpu())
            labels = np.append(labels, label.cpu())
            seqs = np.append(seqs, matrix2seq(data.cpu()))
            # predict manually
            pred = target.gt(0.5).float()  # judge
            correct += pred.eq(label).sum().item()  # accumulate

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        valid_loss / len(valid_dataloader.dataset), correct, len(valid_dataloader.dataset),
        100. * correct / len(valid_dataloader.dataset)))

    # prediction file
    df = pd.DataFrame({'Predict': predictions, 'Label': labels, 'Seqs': seqs})
    df.to_csv('predict_result.csv', index=False)
    # save model threshold
    accuracy = train_utils.acc_score(predictions, labels)
    f1 = train_utils.f1(predictions, labels)
    fpr, tpr, auc_score = train_utils.roc_auc(predictions, labels)
    # result for visualization
    train_utils.all_class_metrics(predictions, labels)
    train_utils.roc_curves(predictions, labels, fold)
    train_utils.pr_curves(predictions, labels, fold)

    return valid_loss/len(valid_dataloader.dataset), accuracy, f1, fpr, tpr, auc_score



def main():
    args = parse_args()
    print(args)

    # ray tune hyper parameter searching
    # 调度器ASHAScheduler会根据指定标准提前中止坏实验
    scheduler = ASHAScheduler(
        metric="accuracy", # metric (str) or loss
        mode="max",    # mode (str) – One of {min, max}.
        grace_period=1,
        reduction_factor=2)
    # Command-line reporter在命令行打印实验报告,指定打印的参数，和关注的值
    reporter = CLIReporter(
        parameter_columns=["l1", "l2", "lr", "batch_size"],
        metric_columns=["loss", "accuracy", "training_iteration"])
    # 指定参数
    config = {
        #"l1": tune.sample_from(lambda _: 2 ** np.random.randint(2, 9)),
        #"l2": tune.sample_from(lambda _: 2 ** np.random.randint(2, 9)),
        "lr": tune.loguniform(1e-4, 1e-1),
        "batch_size": tune.choice([24, 48, 64, 128])
    }
    # 执行训练过程，取值超参数空间，找寻合适的超参
    result = tune.run(
        train,
        config=config,
        num_samples = 50, # 超参数空间中取值的次数
        resources_per_trial={"cpu": 8, "gpu": 1},
        scheduler=scheduler,
        progress_reporter=reporter)

    # 找出最佳实验,last step accuracy max
    best_trial = result.get_best_trial("accuracy", "max", "last")
    # 打印最佳实验的参数配置
    print("Best trial config: {}".format(best_trial.config))
    # 打印最终的验证集的的损失
    print("Best trial final validation loss: {}".format(
        best_trial.last_result["loss"]))
    # 打印最终的验证集的准确性
    print("Best trial final validation accuracy: {}".format(
        best_trial.last_result["accuracy"]))

if __name__ == '__main__':
    main()
