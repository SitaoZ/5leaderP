#!/home/zhusitao/anaconda3/bin/python
# -*- coding:utf-8 -*-
'''
filename: visualFeature.py
date: 2022/3/31 7:15 PM
author: Sitao Zhu
mail: zhusitao1990@163.com
'''


import torch
from aTSS.models import AttenNet



# visual CNN using the kernal size

def load_dict(modelPath):
    model = AttenNet()
    model.load_state_dict(torch.load(modelPath))
    for name, para in model.named_parameters():
        print(type(para), para.size())


if __name__=='__main__':
    load_dict('saved_model.h5')