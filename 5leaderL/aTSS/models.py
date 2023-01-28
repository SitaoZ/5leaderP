#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: models.py
date: 2021/12/26 上午9:42
author: Sitao Zhu
mail: zhusitao1990@163.com
'''

import torch
import torch as t
import numpy as np
from torch import nn
from torch.nn import init
from torch.nn import Sequential
import torch.nn.functional as F
from torch.autograd import Variable




# padding same: padding = dilation * (kernel -1) / 2)

##### classification ######
# GRU
class GruNet(nn.Module):
    """
    aTSS prediction model
    """
    def __init__(self, l1,l2):
        super(GruNet, self).__init__()
        self.layer1 = Sequential(
            nn.Conv1d(4, 128,  # input channel, output channel
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding =1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer2 = Sequential(
            nn.Conv1d(128, 256,
                      kernel_size=5,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=2),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer3 = Sequential(
            nn.Conv1d(256, 256,
                      kernel_size=7,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=3),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer4 = Sequential(
            nn.Conv1d(256, 256,
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.gru = nn.GRU(input_size=256, hidden_size=128, num_layers=2,
                          batch_first=True, bidirectional=True)
        self.fc1 = nn.Linear(256*32, l1)
        self.fc2 = nn.Linear(l1, l2)
        self.fc3 = nn.Linear(l2, 1)

    def forward(self,x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        # gru
        x = torch.transpose(x, 2, 1)
        x ,x_hidden = self.gru(x)
        # x = torch.cat((x1,x2,x3),dim=1) # concat channel
        # flat for Linear layers
        x = x.reshape(x.size(0), -1)
        x = self.fc1(x)
        x = torch.relu(x)
        x = F.dropout(x, p=0.2)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)

        return x

class GruCatNet(nn.Module):
    """
    aTSS prediction model
    """
    def __init__(self, l1,l2):
        super(GruCatNet, self).__init__()
        self.layer1 = Sequential(
            nn.Conv1d(4, 128,  # input channel, output channel
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding =1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer2 = Sequential(
            nn.Conv1d(128, 256,
                      kernel_size=5,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=2),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer3 = Sequential(
            nn.Conv1d(4, 256,
                      kernel_size=7,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=3),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1),
        )
        self.gru = nn.GRU(input_size=256, hidden_size=128, num_layers=1,
                          batch_first=True, bidirectional=True)
        self.fc1 = nn.Linear(256*128, l1)
        self.fc2 = nn.Linear(l1, l2)
        self.fc3 = nn.Linear(l2, 1)

    def forward(self,x):
        x = self.layer1(x)
        x = self.layer2(x)
        # x3 = self.layer3(x)
        # x4 = torch.cat((x1,x2,x3),dim=1) # cat channel
        # gru
        x = torch.transpose(x, 2, 1) # N,C,L --> N,L,C
        x ,x_hidden = self.gru(x)
        # p2 = torch.transpose(p2,2,1)   # N,L,C --> N,C,L
        # x = torch.cat((x,p2),dim=1) # concat channel, dim2=1
        # flat for Linear layers
        x = x.reshape(x.size(0), -1)
        x = self.fc1(x)
        x = torch.relu(x)
        x = F.dropout(x, p=0.2)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)

        return x

# LSTM
class LstmNet(nn.Module):
    """
    aTSS prediction model
    """
    def __init__(self, l1,l2):
        super(LstmNet, self).__init__()
        self.layer1 = Sequential(
            nn.Conv1d(4, 128,  # input channel, output channel
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding =1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer2 = Sequential(
            nn.Conv1d(128, 256,
                      kernel_size=5,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=2),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer3 = Sequential(
            nn.Conv1d(256, 256,
                      kernel_size=7,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=3),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer4 = Sequential(
            nn.Conv1d(256, 256,
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.lstm = nn.LSTM(input_size=256, hidden_size=128, num_layers=2,
                          batch_first=True, bidirectional=True)
        self.fc1 = nn.Linear(256*32, l1)
        self.fc2 = nn.Linear(l1, l2)
        self.fc3 = nn.Linear(l2, 1)

    def forward(self,x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        # gru
        x = torch.transpose(x, 2, 1)
        x ,(hn, cn) = self.lstm(x)
        # x = torch.cat((x1,x2,x3),dim=1) # concat channel
        # flat for Linear layers
        x = x.reshape(x.size(0), -1)
        x = self.fc1(x)
        x = torch.relu(x)
        x = F.dropout(x, p=0.2)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)

        return x

# Attention
class AttenNet(nn.Module):
    """
    cnn + attention
    """
    def __init__(self, num_classes=1, attention=True, normalize_attn=True, init_weights=False):
        super(AttenNet, self).__init__()
        # conv blocks
        self.conv1 = self._make_layer(4, 64, 1)
        self.conv2 = self._make_layer(64, 128, 1)
        self.conv3 = self._make_layer(128, 256, 1)
        self.conv4 = self._make_layer(256, 512, 1)
        self.conv5 = self._make_layer(512, 512, 1)
        self.dense = OneConv(in_features=128, out_features=512)
        # attention blocks
        self.attention = attention
        if self.attention:
            self.att_dense = OneConv(in_features=256, out_features=512)
            self.attn1 = SpatialAttn(in_features=512, normalize_attn=normalize_attn)
            self.attn2 = SpatialAttn(in_features=512, normalize_attn=normalize_attn)
            self.attn3 = SpatialAttn(in_features=512, normalize_attn=normalize_attn)
        # final classification layer
        if self.attention:
            self.classifier = nn.Linear(in_features=512*3, out_features=num_classes, bias=True)
        else:
            self.classifier = nn.Linear(in_features=512, out_features=num_classes, bias=True)
        if init_weights:
            self._initialize_weights()

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        l1 = self.conv3(x)
        l2 = self.conv4(l1)
        l3 = self.conv5(l2)
        g = self.dense(x) # batch_sizex512x1x1
        # attention
        if self.attention:
            c1, g1 = self.attn1(self.att_dense(l1), g)
            c2, g2 = self.attn2(l2, g)
            c3, g3 = self.attn3(l3, g)
            g = torch.cat((g1,g2,g3), dim=1) # batch_sizex3C
            # classification layer
            x = self.classifier(g) # batch_sizexnum_classes
        else:
            c1, c2, c3 = None, None, None
            x = self.classifier(torch.squeeze(g))
        return x

    def _make_layer(self, in_features, out_features, blocks, pool=False):
        layers = []
        for i in range(blocks):
            conv1d = nn.Conv1d(in_channels=in_features, out_channels=out_features, kernel_size=3, padding=1, bias=False)
            layers += [conv1d, nn.BatchNorm1d(out_features), nn.ReLU(inplace=True)]
            in_features = out_features
            if pool:
                layers += [nn.MaxPool1d(kernel_size=1, stride=1)]
        return nn.Sequential(*layers)

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv1d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

class OneConv(nn.Module):
    """ 1x1 conv 用来进行升、降特征的维度(通道数)，不改变尺寸"""
    def __init__(self, in_features, out_features):
        super(OneConv, self).__init__()
        self.layer = nn.Conv1d(in_channels=in_features,
                               out_channels=out_features,
                               kernel_size=1, padding=0,
                               bias=False)

    def forward(self, x):
        return self.layer(x)

# Spatial Attention mechanism
class SpatialAttn(nn.Module):
    """空间卷积"""
    def __init__(self, in_features, normalize_attn=True):
        super(SpatialAttn, self).__init__()
        self.normalize_attn = normalize_attn
        self.op = nn.Conv1d(in_channels=in_features, out_channels=1,
            kernel_size=1, padding=0, bias=False)

    def forward(self, l, g):
        N, C, L = l.size()
        c = self.op(l+g) # (batch_size,1,L)
        if self.normalize_attn:
            a = F.softmax(c.view(N,1,-1), dim=2).view(N,1,L)
        else:
            a = torch.sigmoid(c)
        # attention calulate
        g = torch.mul(a.expand_as(l), l)
        if self.normalize_attn:
            g = g.view(N,C,-1).sum(dim=2) # (batch_size,C)
        else:
            g = F.adaptive_avg_pool1d(g, (1,1)).view(N,C)
        return c.view(N,1,L), g

# CNN
class CnnNet(nn.Module):
    """
    CNN model
    """
    def __init__(self, l1=128,l2=64):
        super(CnnNet, self).__init__()
        self.layer1 = Sequential(
            nn.Conv1d(4, 128,  # input channel, output channel
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding =1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer2 = Sequential(
            nn.Conv1d(128, 256,
                      kernel_size=5,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=2),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer3 = Sequential(
            nn.Conv1d(256, 256,
                      kernel_size=7,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=3),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer4 = Sequential(
            nn.Conv1d(256, 256,
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.fc1 = nn.Linear(256*32, l1)
        self.fc2 = nn.Linear(l1, l2)
        self.fc3 = nn.Linear(l2, 1)

    def forward(self,x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        # x = torch.cat((x1,x2,x3),dim=1) # concat channel
        # flat for Linear layers
        x = x.reshape(x.size(0), -1)
        x = self.fc1(x)
        x = torch.relu(x)
        x = F.dropout(x, p=0.2)
        x = self.fc2(x)
        x = torch.relu(x)
        x = F.dropout(x, p=0.2)
        x = self.fc3(x)

        return x


class ResBlock(nn.Module):
    """
    ResBlock module
    """
    def __init__(self,channel_in,channel_out,stride,kernel_size,padding_size,shortcut=None,pool=False):
        super(ResBlock,self).__init__()
        self.left = nn.Sequential(
            nn.Conv1d(channel_in,channel_out,
                      kernel_size=kernel_size,
                      padding=padding_size,
                      bias=True),
            nn.BatchNorm1d(channel_out),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.2),
            nn.Conv1d(channel_out,channel_out,
                      kernel_size=kernel_size,
                      padding=padding_size,
                      bias=True),
            nn.BatchNorm1d(channel_out)
        )
        self.right = shortcut
        self.pool = pool
        self.MaxPool = nn.MaxPool1d(kernel_size=2, stride=2)
    def forward(self,x):
        out = self.left(x)
        residual = x if self.right is None else self.right(x)
        out += residual
        out = F.relu(out)
        if self.pool:
            out = self.MaxPool(out)

        return out

# ResNet
class ResNet(nn.Module):
    def __init__(self):
        super(ResNet, self).__init__()
        # 512/2/2/2 = 64
        self.layer1 = self.make_layer(channel_in=4, channel_out=128, block_num=3, kernel_size=3, padding_size=1,
                                      stride=1)
        # 64/2/2/2 = 8
        self.layer2 = self.make_layer(channel_in=128, channel_out=128, block_num=3, kernel_size=3, padding_size=1,
                                      stride=1)
        # 8/2/2/2 = 1
        self.layer3 = self.make_layer(channel_in=128, channel_out=256, block_num=3, kernel_size=3, padding_size=1,
                                      stride=1, pool=False)
        # self.dropout = nn.Dropout(0.5)
        self.flatten = torch.nn.Flatten()
        self.ff1 = nn.Linear(2048, 32, bias=True)
        self.ff2 = nn.Linear(32, 1, bias=True)
    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.flatten(x)
        x = self.ff1(x) 
        # x = F.relu(x)  # x = t.tanh(x)
        x = t.tanh(x)
        x = F.dropout(x, p=0.2)
        x = self.ff2(x)
        return x
    
    def make_layer(self,channel_in,channel_out,block_num,kernel_size,padding_size,stride=1,pool=True):
        '''
        build many resnet block
        :return: residual block
        '''

        shortcut = self.conv_layer(channel_in ,channel_out, kernel_size=3, padding_size=1, dilation=1)
        layers = []
        # 第一层在不同resblock 之间传递，改变block之间channel不一致的情况
        layers.append(ResBlock(channel_in,channel_out,stride,kernel_size,padding_size,shortcut,pool=pool))
        # resnet core
        for i in range(1,block_num):
            layers.append(ResBlock(channel_out,channel_out,stride,kernel_size,padding_size,pool=pool))

        return nn.Sequential(*layers)

    def conv_layer(self, chann_in, chann_out, kernel_size, padding_size, dilation):
        layer = nn.Sequential(
            nn.Conv1d(chann_in, chann_out,
                      kernel_size=kernel_size,
                      padding=padding_size,
                      stride=1,
                      dilation=dilation,
                      groups=1,
                      bias=True),
            nn.BatchNorm1d(chann_out),
            nn.ReLU(),
            nn.Dropout(p=0.1)
            )
        return layer



################################################################################################# regression #########################################################


# RegResNet
class RegResNet(nn.Module):
    def __init__(self, l1, l2):
        super(RegResNet, self).__init__()
        # 512/2/2/2 = 64 128
        self.layer1 = self.make_layer(channel_in=4, channel_out=128, block_num=2, kernel_size=3, padding_size=1,
                                      stride=1)
        # 64/2/2/2 = 8 32
        self.layer2 = self.make_layer(channel_in=128, channel_out=256, block_num=2, kernel_size=3, padding_size=1,
                                      stride=1)
        # 8/2/2/2 = 1 8
        self.layer3 = self.make_layer(channel_in=256, channel_out=512, block_num=2, kernel_size=3, padding_size=1,
                                      stride=1)
        # self.dropout = nn.Dropout(0.5)
        # self.leak = nn.LeakyReLU(0.01)
        self.flatten = torch.nn.Flatten()
        self.fc1 = nn.Linear(512*8, l1, bias=True)
        self.fc2 = nn.Linear(l1, l2, bias=True)
        self.fc3 = nn.Linear(l2, 1, bias=True)
    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.flatten(x)
        x = self.fc1(x)
        x = t.tanh(x) # x = F.relu(x)  # x = t.tanh(x)
        x = F.dropout(x, p=0.2)
        x = self.fc2(x)
        x = t.tanh(x) # x = t.tanh(x) # x = F.relu(x)
        x = self.fc3(x)
        
        return x
    def model_name(self):
        return 'RegResNet'
    def make_layer(self,channel_in,channel_out,block_num,kernel_size,padding_size,stride=1,pool=True):
        '''
        build many resnet block
        :return: residual block
        '''

        shortcut = self.conv_layer(channel_in ,channel_out, kernel_size=3, padding_size=1, dilation=1)
        layers = []
        # 第一层在不同resblock 之间传递，改变block之间channel不一致的情况
        layers.append(ResBlock(channel_in,channel_out,stride,kernel_size,padding_size,shortcut,pool=pool))
        # resnet core
        for i in range(1,block_num):
            layers.append(ResBlock(channel_out,channel_out,stride,kernel_size,padding_size,pool=pool))

        return nn.Sequential(*layers)

    def conv_layer(self, chann_in, chann_out, kernel_size, padding_size, dilation):
        layer = nn.Sequential(
            nn.Conv1d(chann_in, chann_out,
                      kernel_size=kernel_size,
                      padding=padding_size,
                      stride=1,
                      dilation=dilation,
                      groups=1,
                      bias=True),
            nn.BatchNorm1d(chann_out),
            nn.ReLU(),
            nn.Dropout(p=0.2)
            )
        return layer


# CNN for regression
class RegCnnNet(nn.Module):
    """
    aTSS prediction model
    """
    def __init__(self, l1, l2):
        super(RegCnnNet, self).__init__()
        self.layer1 = Sequential(
            nn.Conv1d(4, 128,  # input channel, output channel
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding =1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer2 = Sequential(
            nn.Conv1d(128, 128,
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer3 = Sequential(
            nn.Conv1d(128, 256,
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.layer4 = Sequential(
            nn.Conv1d(256, 256,
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.1)
        )
        self.fc1 = nn.Linear(256*32, l1)
        self.fc2 = nn.Linear(l1, l2)
        self.fc3 = nn.Linear(l2, 1)

    def forward(self,x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        # flat for Linear layers
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = t.tanh(x) # x = F.gelu(x)
        x = F.dropout(x, p=0.2)
        x = self.fc2(x)
        x = t.tanh(x) # x = F.gelu(x)
        x = self.fc3(x)

        return x
    def model_name(self):
        return 'RegCnnNet'

# GRU for regression
class RegGruNet(nn.Module):
    """
    aTSS prediction model
    """
    def __init__(self, l1, l2):
        super(RegGruNet, self).__init__()
        self.layer1 = Sequential(
            nn.Conv1d(4, 128,  # input channel, output channel
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.2)
        )
        self.layer2 = Sequential(
            nn.Conv1d(128, 256,
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.2)
        )
        self.layer3 = Sequential(
            nn.Conv1d(256, 256,
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.2)
        )
        self.layer4 = Sequential(
            nn.Conv1d(256, 256,
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.2)
        )
        self.gru = nn.GRU(input_size=256, hidden_size=128, num_layers=2,
                          batch_first=True, bidirectional=True)
        self.fc1 = nn.Linear(256 * 32, l1)
        self.fc2 = nn.Linear(l1, l2)
        self.fc3 = nn.Linear(l2, 1)

    def forward(self,x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)     # N,C,L
        # Revert channel dimension
        x = x.permute(0, 2, 1) # N,L,C
        x, x_hidden = self.gru(x)
        # x = torch.cat((x1,x2,x3),dim=1) # concat channel
        # flat for Linear layers
        x = x.reshape(x.size(0), -1)
        x = self.fc1(x)
        x = t.tanh(x) # x = F.gelu(x) # activation function relu
        x = F.dropout(x, p=0.2)
        x = self.fc2(x)
        x = t.tanh(x) # x = F.gelu(x) # relu
        x = F.dropout(x, p=0.2)
        x = self.fc3(x)

        return x
    def model_name(self):
        return 'RegGruNet'


# LSTM for regression 
class RegLstmNet(nn.Module):
    """
    aTSS prediction model
    """
    def __init__(self, l1, l2):
        super(RegLstmNet, self).__init__()
        self.layer1 = Sequential(
            nn.Conv1d(4, 128,  # input channel, output channel
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.2)
        )
        self.layer2 = Sequential(
            nn.Conv1d(128, 256,
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.2)
        )
        self.layer3 = Sequential(
            nn.Conv1d(256, 256,
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.2)
        )
        self.layer4 = Sequential(
            nn.Conv1d(256, 256,
                      kernel_size=3,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.2)
        )
        self.lstm = nn.LSTM(input_size=256, hidden_size=128, num_layers=2,
                          batch_first=True, bidirectional=True)
        self.fc1 = nn.Linear(256 * 32, l1)
        self.fc2 = nn.Linear(l1, l2)
        self.fc3 = nn.Linear(l2, 1)

    def forward(self,x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)     # N,C,L
        # Revert channel dimension
        x = x.permute(0, 2, 1) # N,L,C
        x, x_hidden = self.lstm(x)
        # x = torch.cat((x1,x2,x3),dim=1) # concat channel
        # flat for Linear layers
        x = x.reshape(x.size(0), -1)
        x = self.fc1(x)
        x = t.tanh(x) # x = F.gelu(x) # activation function relu
        x = F.dropout(x, p=0.2)
        x = self.fc2(x)
        x = t.tanh(x) # x = F.gelu(x) # relu
        x = F.dropout(x, p=0.2)
        x = self.fc3(x)

        return x
    def model_name(self):
        return 'RegLstmNet'

# Attention for regression
class RegAttenNet(nn.Module):
    """
    cnn + attention
    """
    def __init__(self, attention=True, normalize_attn=True, init_weights=False):
        super(RegAttenNet, self).__init__()
        # conv blocks
        self.conv1 = self._make_layer(4, 64, 1)
        self.conv2 = self._make_layer(64, 128, 1)
        self.conv3 = self._make_layer(128, 256, 1)
        self.conv4 = self._make_layer(256, 512, 1)
        self.conv5 = self._make_layer(512, 512, 1)
        self.dense = OneConv(in_features=128, out_features=512)
        # attention blocks
        self.attention = attention
        if self.attention:
            self.att_dense = OneConv(in_features=256, out_features=512)
            self.attn1 = SpatialAttn(in_features=512, normalize_attn=normalize_attn)
            self.attn2 = SpatialAttn(in_features=512, normalize_attn=normalize_attn)
            self.attn3 = SpatialAttn(in_features=512, normalize_attn=normalize_attn)
        # FC layer
        if self.attention:
            self.regress = nn.Linear(in_features=512*3, out_features=30, bias=True)
        else:
            self.regress = nn.Linear(in_features=512, out_features=30, bias=True)
        self.fc = nn.Linear(in_features=30, out_features=1, bias=True)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        l1 = self.conv3(x)
        l2 = self.conv4(l1)
        l3 = self.conv5(l2)
        g = self.dense(x) # batch_sizex512x1x1
        # attention
        if self.attention:
            c1, g1 = self.attn1(self.att_dense(l1), g)
            c2, g2 = self.attn2(l2, g)
            c3, g3 = self.attn3(l3, g)
            g = torch.cat((g1,g2,g3), dim=1) # batch_sizex3C
            # classification layer
            x = self.regress(g) # batch_sizexnum_classes
            x = t.tanh(x) # x = F.relu(x) # relu
            x = F.dropout(x, p=0.2)
            x = self.fc(x)
        else:
            c1, c2, c3 = None, None, None
            x = self.regress(torch.squeeze(g))
            x = F.relu(x) # relu
            x = F.dropout(x, p=0.2)
            x = self.fc(x)
        return x
    def model_name(self):
        return 'RegAttenNet'
    
    def _make_layer(self, in_features, out_features, blocks, pool=False):
        layers = []
        for i in range(blocks):
            conv1d = nn.Conv1d(in_channels=in_features, out_channels=out_features, kernel_size=3, padding=1, bias=False)
            layers += [conv1d, nn.BatchNorm1d(out_features), nn.ReLU(inplace=True)]
            in_features = out_features
            if pool:
                layers += [nn.MaxPool1d(kernel_size=1, stride=1)]
        return nn.Sequential(*layers)
    
    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv1d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)


##### LR #####
class LogisticRegression(torch.nn.Module):
    def __init__(self, input_dim=4*512, output_dim=1):
        super(LogisticRegression, self).__init__()
        self.linear = torch.nn.Linear(input_dim, output_dim)
    def forward(self, x):
        # outputs = torch.sigmoid(self.linear(x))
        x = x.reshape(-1, 4*512)
        outputs = self.linear(x) # sigmoid function add in loss function
        return outputs


if __name__=='__main__':
    from torchsummary import summary
    # model = CnnNet(128, 64)
    # model = GruNet(256, 128)
    # model = LstmNet(256, 128)
    # model = ResNet()
    # model = GruCatNet(32,10)
    # model = RegGruNet(256, 128)
    # model = AttenNet(num_classes=1)
    # model = RegAttenNet()
    # model = RegResNet()
    # print(model.model_name())
    model = RegCnnNet(256, 128)
    summary(model)
