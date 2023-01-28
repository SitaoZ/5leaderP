#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: train.py
date: 2022/3/3 9:30 AM
author: Sitao Zhu
mail: zhusitao1990@163.com
'''

# basic
import os
import time
import argparse
import random
import numpy as np
import pandas as pd
# torch
import torch
from torch import nn
from torch.utils.data import DataLoader
# model
from aTSS import train_utils
from aTSS.dataset import dataset
from aTSS.models import GruNet, LstmNet
from aTSS.models import CnnNet, AttenNet
from aTSS.models import LogisticRegression, ResNet
from aTSS.preprocessing import matrix2seq, shuffle_arrays
# plot
import seaborn as sns
import matplotlib.pyplot as plt
# sklearn
from sklearn.metrics import auc
from sklearn.model_selection import KFold
from sklearn.metrics import precision_recall_curve
from sklearn.model_selection import train_test_split

plt.rcParams.update({'figure.max_open_warning': 0})


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





Models = {
    'cnn': CnnNet(256, 128),
    'lr': LogisticRegression(),
    'gru': GruNet(256, 128),
    'lstm': LstmNet(256, 128),
    'attention':AttenNet(),
    'resnet': ResNet()
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

def parse_args():
    parser = argparse.ArgumentParser(description='PyTorch Implementation of TSAR Predict')

    parser.add_argument('--model', type=str, help='model name',
                        choices=['lr','cnn','gru','lstm','attention','resnet'])
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
    parser.add_argument('--test_data_path', type=str,
                        default='test_class_data.npy',
                        help='test data saved in numpy ndarry')
    parser.add_argument('--test_label_path', type=str,
                        default='test_class_label.npy',
                        help='test label saved in numpy ndarray')

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



def shuffle_train_test(train_data_array, train_label_array, test_data_array, test_label_array):
    train_num = train_data_array.shape[0]
    test_num = test_data_array.shape[0]

    data = np.concatenate((train_data_array, test_data_array),axis=0)
    label = np.concatenate((train_label_array, test_label_array),axis=0)
    data_shuffle, label_shuffle = shuffle_arrays(data,label)
    ratio = test_num/(train_num+test_num)
    train_data, test_data, train_label, test_label = train_test_split(data_shuffle,
                                                                      label_shuffle,
                                                                      test_size=ratio,
                                                                      random_state=42)

    return train_data, train_label, test_data, test_label


def merge_train_test(train_data_array, train_label_array, test_data_array, test_label_array):
    data = np.concatenate((train_data_array, test_data_array), axis=0)
    label = np.concatenate((train_label_array, test_label_array), axis=0)
    return data, label

def train(config, checkpoint_dir = None):
    """
    Train model and validate in every epoch
    :param config: configuare file for train
    :param checkpoint_dir: model to load
    :return:
    """
    # seed
    seed_torch(12)
    # step1 data
    train_data_array = np.load(config.train_data_path)
    train_label_array = np.load(config.train_label_path)

    # load saved model if exist
    if checkpoint_dir:
        model_state = torch.load(os.path.join(checkpoint_dir, "rice.h5"))
        model.load_state_dict(model_state)
    # cross fold roc curve
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 1000)
    # cross fold pr curve
    y_real = []
    y_proab = []
    # Kfold cross validation
    fig, (ax_roc, ax_pr) = plt.subplots(2)
    auc_score_kfold = 0
    kfold = KFold(n_splits=10, shuffle=True)
    for fold, (train_index, valid_index) in enumerate(kfold.split(train_data_array)):
        # Early stopping instance
        early_stopping = EarlyStopping()
        # step 2 Satisfaction Index
        min_valid_loss = np.inf # positive infinity
        max_accuracy = np.NINF  # negative infinity
        max_f1_score = np.NINF
        max_auc = np.NINF
        # step 3 model instance
        model = Models[config.model]
        print(model)
        model.apply(init_weights)
        if torch.cuda.is_available():
            model.cuda()

        # step 4 loss function and optimizer
        criterion = nn.BCEWithLogitsLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=config.lr, betas=(0.9, 0.999))
        # learning rate decay
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=30,
                                                    gamma=0.5, verbose=True)

        train_data, valid_data = train_data_array[train_index], train_data_array[valid_index]
        train_label, valid_label = train_label_array[train_index], train_label_array[valid_index]

        # train set
        train_set = dataset(train_data, train_label, train=True)
        train_dataloader = DataLoader(dataset=train_set,
                                      batch_size=config.batch_size,
                                      shuffle=True,
                                      num_workers=2)
        # valid set
        valid_set = dataset(valid_data, valid_label, train=True)
        valid_dataloader = DataLoader(dataset=valid_set,
                                      batch_size=24,
                                      shuffle=True,
                                      num_workers=2)
        for e in range(1, config.epoch+1):
            train_loss = 0.0
            model.train() # set flag in Dropout and BatchNorm
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
                    print(f'{fold+1} Fold '
                          f'{time.strftime("%y%m%d_%H:%M:%S")} train epoch {e}'
                          f'[{batch_idx}/{len(train_dataloader)}] '
                          f'({100*batch_idx/len(train_dataloader):.0f}%)\t'
                          f'{train_loss:.6f}')
            scheduler.step()  # learning rate decay
            # step5 valid
            # valid_loss, accuracy , f1, fpr, tpr, auc_score = valid(valid_dataloader, model, criterion, fold+1)
            fpr, tpr, auc_score, predictions, labels, validation_loss = valid(valid_dataloader, model, criterion, fold+1)
            # Early stopping
            early_stopping(validation_loss, model)
            if early_stopping.early_stop:
                print(f"Early stopping at epoch {e}")
                # roc and pr curve in last epoch
                interp_tpr = np.interp(mean_fpr, fpr, tpr)
                interp_tpr[0] = 0.0
                tprs.append(interp_tpr)
                aucs.append(auc_score)
                ax_roc.plot(
                    fpr,
                    tpr,
                    color=sns.color_palette("Set3", 12)[fold-1],
                    label=r"ROC Fold %i (AUC = %0.2f)" % (fold, auc_score),
                    lw=1,
                    alpha=0.8,
                )
                # pr curve
                y_real.append(labels)
                y_proab.append(predictions)
                precision, recall, thresholds = train_utils.pr(predictions, labels)
                ax_pr.plot(
                    recall,
                    precision,
                    color=sns.color_palette("Set3", 12)[fold-1],
                    label=r"PR Fold %i " % (fold),
                    lw=1,
                    alpha=0.8,
                )
                # save model
                torch.save(model.state_dict(), 'saved_model.h5')
                test(config, valid_dataloader, fold+1)
                break 
    # mean of ten fold validation
    ax_roc.plot([0, 1], [0, 1], linestyle="--", lw=2, color="r", label="Chance", alpha=0.8)
    # ROC and data
    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    ax_roc.plot(
        mean_fpr,
        mean_tpr,
        'k--',
        label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
        lw=2,
        alpha=0.8,
    )
    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    ax_roc.fill_between(
        mean_fpr,
        tprs_lower,
        tprs_upper,
        color="grey",
        alpha=0.2,
        label=r"$\pm$ 1 std. dev.",
    )
    ax_roc.set(
        xlim=[-0.05, 1.05],
        ylim=[-0.05, 1.05],
        title="ROC Curver",
        xlabel='False Positive Rate (1-Specificity)',
        ylabel='True Positive Rate (Sensitivity)'
    )
    ax_roc.legend(loc="lower right")
    fig.savefig('Mean_ROC.png')
    df_mean = pd.DataFrame(dict(fpr=mean_fpr, tpr=mean_tpr))
    df_mean.to_csv('ROC_Curve_mean_data.csv', index=False)

    # PR and data
    y_real = np.concatenate(y_real)
    y_proab = np.concatenate(y_proab)
    precision, recall, _ = precision_recall_curve(y_real, y_proab)
    ax_pr.plot(
        recall,
        precision,
        'k--',
        label=r"Mean PR",
        lw=2,
        alpha=0.8,
    )

    ax_pr.set(
        xlim=[-0.05, 1.05],
        ylim=[-0.05, 1.05],
        title="Precision-Recall Curver",
        xlabel='Recall',
        ylabel='Precision'
    )
    fig.savefig('Mean_PR.png')
    df_mean = pd.DataFrame(dict(recall=recall, precision=precision))
    df_mean.to_csv('PR_Curve_mean_data.csv', index=False)


def valid(valid_dataloader, model, criterion, fold):
    """
    Validate the training model in every epoch
    :param valid_dataloader: valid dataloader
    :param model: model
    :param criterion:
    :param fold:
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
            pred = target.gt(0.5).float()           # judge
            correct += pred.eq(label).sum().item()  # accumulate
    validation_loss = valid_loss / len(valid_dataloader.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        valid_loss / len(valid_dataloader.dataset), correct, len(valid_dataloader.dataset),
        100. * correct / len(valid_dataloader.dataset)))

    # prediction file
    df = pd.DataFrame({'Predict': predictions, 'Label': labels, 'Seqs': seqs})
    df.to_csv('predict_result.csv', index=False)
    # save model threshold
    accuracy = train_utils.acc_score(predictions, labels)
    f1 = train_utils.f1(predictions, labels)
    # roc
    fpr, tpr, auc_score = train_utils.roc_auc(predictions, labels)
    # pr
    precision, recall, thresholds = train_utils.pr(predictions, labels)
    # result for visualization
    train_utils.all_class_metrics(predictions, labels)
    train_utils.roc_curves(predictions, labels, fold)
    train_utils.pr_curves(predictions, labels, fold)

    # return valid_loss/len(valid_dataloader.dataset), accuracy, f1, fpr, tpr, auc_score
    return fpr, tpr, auc_score, predictions, labels, validation_loss

def test(config, test_dataloader, fold):
    """
    Test the trained model
    :param config:
    :param test_dataloader:
    :param fold:
    :return:
    """
    # step1 model load
    model = Models[config.model]
    model.load_state_dict(torch.load('saved_model.h5'))

    # cuda
    if torch.cuda.is_available():
        model.cuda()

    # step3 loss function
    criterion = nn.BCEWithLogitsLoss()

    test_loss = 0.0
    correct = 0
    predictions = np.array([])
    labels = np.array([])
    seqs = np.array([])

    model.eval()
    with torch.no_grad():
        for data, label in test_dataloader:
            if torch.cuda.is_available():
                data, label = data.cuda(), label.cuda()
            # forward
            # data = data.reshape(-1, 4*512)
            target = model(data)
            target = target.squeeze(1)
            # loss cal
            loss = criterion(target, label)
            # accumulate loss
            test_loss += loss.item() * data.size(0)
            # prediction accuracy
            pred = torch.sigmoid(target)
            predictions = np.append(predictions, pred.cpu())
            labels = np.append(labels, label.cpu())
            seqs = np.append(seqs, matrix2seq(data.cpu()))
            pred = target.gt(0.5).float() # judge
            correct += pred.eq(label).sum().item() # accumulate
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
            test_loss/len(test_dataloader.dataset), correct, len(test_dataloader.dataset),
            100. * correct / len(test_dataloader.dataset)))
    df = pd.DataFrame({'Predict':predictions,'Label':labels,'Seqs':seqs})
    df.to_csv('predict_result.csv', index=False)
    train_utils.all_class_metrics(predictions, labels)
    train_utils.roc_curves(predictions, labels, fold)
    train_utils.pr_curves(predictions, labels, fold)


def main():
    config = parse_args()
    print(config)
    # step1 training
    train(config)





if __name__ == '__main__':
    main()
