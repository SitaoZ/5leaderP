#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: test.py
date: 2022/3/3 3:20 PM
author: Sitao Zhu
mail: zhusitao1990@163.com
'''

# basic
import argparse
import numpy as np
import pandas as pd
# torch
import torch
from torch import nn
from torch.utils.data import DataLoader
# model
from aTSS import train_utils
from aTSS.dataset import dataset
from aTSS.models import LogisticRegression
from aTSS.models import CnnNet, AttenNet
from aTSS.models import GruNet, LstmNet
from aTSS.preprocessing import matrix2seq



Models = {
    'cnn': CnnNet(256, 128),
    'lr': LogisticRegression(),
    'gru': GruNet(256, 128),
    'lstm': LstmNet(256, 128),
    'attention':AttenNet(),
}

def parse_args():
    parser = argparse.ArgumentParser(description='PyTorch Implementation of TSAR Predict')

    parser.add_argument('--model', type=str, help='model name',
                        choices=['lr','cnn','gru','lstm','attention'])
    parser.add_argument('--test_data_path', type=str,
                        default='test_class_data.npy',
                        help='test data saved in numpy ndarry')
    parser.add_argument('--test_label_path', type=str,
                        default='test_class_label.npy',
                        help='test label saved in numpy ndarray')
    parser.add_argument('--model_dict_path', type=str, help='model saved name')
    return parser.parse_args()


def test(config):
    """
    Test the trained model
    :param config: parameters config
    :return:
    """
    # step1 model load
    model = Models[config.model]
    model.load_state_dict(torch.load(config.model_dict_path))

    # setp2 test data
    test_data_array = np.load(config.test_data_path)
    test_label_array = np.load(config.test_label_path)
    test_set = dataset(test_data_array, test_label_array, train=False)
    test_dataloader = DataLoader(dataset=test_set,
                                 batch_size=24,
                                 shuffle=True,
                                 num_workers=2)

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
    train_utils.roc_curves(predictions, labels)
    train_utils.pr_curves(predictions, labels)


def main():
    config = parse_args()
    print(config)
    test(config)


if __name__ == '__main__':
    main()
