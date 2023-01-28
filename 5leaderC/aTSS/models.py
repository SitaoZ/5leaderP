#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: models.py
date: 2021/12/26 上午9:42
author: Sitao Zhu
mail: zhusitao1990@163.com
'''

import torch
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
            nn.Dropout(p=0.3),
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
        x = F.relu(x)  # x = t.tanh(x)
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
            nn.Dropout(p=0.3)
            )
        return layer



##### regression ######

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
            # nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.2)
        )
        self.layer2 = Sequential(
            nn.Conv1d(128, 128,
                      kernel_size=5,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=2),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            # nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.2)
        )
        self.layer3 = Sequential(
            nn.Conv1d(128, 128,
                      kernel_size=5,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=2),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            # nn.MaxPool1d(kernel_size=2, stride=2, dilation=1, padding=0),
            nn.Dropout(p=0.2)
        )
        self.fc1 = nn.Linear(128*512, l1)
        self.fc2 = nn.Linear(l1, l2)
        self.fc3 = nn.Linear(l2, 1)

    def forward(self,x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        # flat for Linear layers
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = torch.relu(x)
        x = F.dropout(x, p=0.2)
        x = self.fc2(x)
        x = torch.relu(x)
        x = self.fc3(x)

        return x

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
                      kernel_size=5,
                      stride=1,
                      dilation=1,
                      groups=1,
                      bias=True,
                      padding=2),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            nn.Dropout(p=0.2)
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
        x = F.gelu(x) # activation function relu
        x = F.dropout(x, p=0.2)
        x = self.fc2(x)
        x = F.gelu(x) # relu
        x = F.dropout(x, p=0.2)
        x = self.fc3(x)

        return x

# Attention
class ScaledDotProductAttention(nn.Module):
    '''
    Scaled dot-product attention
    '''

    def __init__(self, d_model, d_k, d_v, h, dropout=.1):
        '''
        :param d_model: Output dimensionality of the model
        :param d_k: Dimensionality of queries and keys
        :param d_v: Dimensionality of values
        :param h: Number of heads
        '''
        super(ScaledDotProductAttention, self).__init__()
        self.fc_q = nn.Linear(d_model, h * d_k)
        self.fc_k = nn.Linear(d_model, h * d_k)
        self.fc_v = nn.Linear(d_model, h * d_v)
        self.fc_o = nn.Linear(h * d_v, d_model)
        self.dropout=nn.Dropout(dropout)

        self.d_model = d_model
        self.d_k = d_k
        self.d_v = d_v
        self.h = h

        # self.init_weights()


    def init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                init.kaiming_normal_(m.weight, mode='fan_out')
                if m.bias is not None:
                    init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                init.constant_(m.weight, 1)
                init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                init.normal_(m.weight, std=0.001)
                if m.bias is not None:
                    init.constant_(m.bias, 0)

    def forward(self, queries, keys, values, attention_mask=None, attention_weights=None):
        '''
        Computes
        :param queries: Queries (b_s, nq, d_model)
        :param keys: Keys (b_s, nk, d_model)
        :param values: Values (b_s, nk, d_model)
        :param attention_mask: Mask over attention values (b_s, h, nq, nk). True indicates masking.
        :param attention_weights: Multiplicative weights for attention values (b_s, h, nq, nk).
        :return:
        '''
        # N,L,C
        b_s, nq = queries.shape[:2]
        nk = keys.shape[1]

        q = self.fc_q(queries).view(b_s, nq, self.h, self.d_k).permute(0, 2, 1, 3)  # (b_s, h, nq, d_k)
        k = self.fc_k(keys).view(b_s, nk, self.h, self.d_k).permute(0, 2, 3, 1)     # (b_s, h, d_k, nk)
        v = self.fc_v(values).view(b_s, nk, self.h, self.d_v).permute(0, 2, 1, 3)   # (b_s, h, nk, d_v)

        att = torch.matmul(q, k) / np.sqrt(self.d_k)  # (b_s, h, nq, nk)
        if attention_weights is not None:
            att = att * attention_weights
        if attention_mask is not None:
            att = att.masked_fill(attention_mask, -np.inf)
        att = torch.softmax(att, -1)
        att=self.dropout(att)

        out = torch.matmul(att, v).permute(0, 2, 1, 3).contiguous().view(b_s, nq, self.h * self.d_v)  # (b_s, nq, h*d_v)
        out = self.fc_o(out)  # (b_s, nq, d_model)
        return out

# Attention for regression
class RegAttenNet(nn.Module):
    def __init__(self):
        super(RegAttenNet, self).__init__()
        # conv blocks
        # self.conv1 = self._make_layer(4, 64, 1, kernel_size=3, padding=1, pool=True)
        # self.conv2 = self._make_layer(64, 128, 1, kernel_size=3, padding=1, pool=True)
        # self.conv3 = self._make_layer(128, 256, 1, kernel_size=3, padding=1, pool=True) # N,256,512
        # self.conv4 = self._make_layer(256, 512, 1, kernel_size=3, padding=1, pool=True)
        self.res1 = self._make_resblock(4, 64, 1, kernel_size=3, padding=1, stride=1, pool=False)
        self.res2 = self._make_resblock(64, 128, 1, kernel_size=5, padding=2, stride=1, pool=False)
        self.res3 = self._make_resblock(128, 256, 1, kernel_size=7, padding=3, stride=1, pool=True)
        # self.atten = ScaledDotProductAttention(256, 256, 256, 3)
        #
        self.gru = nn.GRU(input_size=256, hidden_size=128, num_layers=2,
                          batch_first=True, bidirectional=True)
        self.fc1 = nn.Linear(256*256, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32,1)
        self._initialize_weights()
    def forward(self, x):
        # x = self.conv1(x)
        # x = self.conv2(x)
        # x = self.conv3(x) # N,C,L
        # x = self.conv4(x)
        # x = torch.cat((x1,x2,x3),dim=1)
        # Revert the Channel dimension
        x = self.res1(x)
        x = self.res2(x)
        x = self.res3(x)
        x = x.permute(0, 2, 1) # N,L,C
        # x = self.atten(x, x, x)
        x, x_hidden = self.gru(x)
        x = x.reshape(x.size(0), -1)
        x = self.fc1(x)
        x = F.dropout(x, p=0.2)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        return x

    def _make_layer(self, in_features, out_features, blocks, kernel_size=3, padding=1, pool=False):
        layers = []
        for i in range(blocks):
            conv1d = nn.Conv1d(in_channels=in_features, out_channels=out_features,
                               kernel_size=kernel_size, padding=padding, bias=False)
            layers += [conv1d, nn.BatchNorm1d(out_features), nn.ReLU(inplace=True),nn.Dropout(p=0.2)]
            in_features = out_features
            if pool:
                layers += [nn.MaxPool1d(kernel_size=2, stride=2)]
        return nn.Sequential(*layers)

    def _make_resblock(self, in_features, out_features, blocks, kernel_size=3, padding=1, stride=1, pool=False):
        layer = []
        for i in range(blocks):
            shortcut = nn.Conv1d(in_features, out_features, kernel_size=3, padding=1, dilation=1)
            layer.append(ResBlock(in_features,out_features,stride,kernel_size,padding,shortcut=shortcut,pool=pool))
            in_features = out_features

        return nn.Sequential(*layer)



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
    model = ResNet()
    summary(model)
