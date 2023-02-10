# 5'leaderP
5' end predictor (5′leaderP) can use different neural networks to classify (i.e., 5'leaderC, 5' leader classifier model) and locate the aTSS regions (i.e., 5'leaderL, 5' leader locator model)


## Brief introduction of 5'leaderP package

### Install
Two way offer to install 5'leaderP module.

#### install command line

```bash
git clone https://github.com/SitaoZ/5leaderP.git
```

#### Requirements

python >= 3.7.6 [python](https://www.python.org/)  
pandas >= 1.2.4 [pandas](https://pandas.pydata.org/docs/)  
gffutils >= 0.10.1 [gffutils](https://pythonhosted.org/gffutils/)  
setuptools >= 49.2.0 [setuptools](https://pypi.org/project/setuptools/)  
biopython >= 1.78 [biopython](https://biopython.org/wiki/Documentation/)  
details see requirements.txt

### Usage
5'leaderC is used to determine if the sequence contains aTSS site. 5'leaderL determines the specific location of the aTSS.

#### 5'leaderC

```bash
python train5leaderC.py -h 
usage: train5leaderC.py [-h] [--model {lr,cnn,gru,lstm,attention,resnet}] [--train_data_path TRAIN_DATA_PATH]
                        [--train_label_path TRAIN_LABEL_PATH] [--batch_size BATCH_SIZE] [--epoch EPOCH] [--lr LR] [--lr_decay LR_DECAY]
                        [--model_saved MODEL_SAVED]

PyTorch Implementation of aTSS Predict

optional arguments:
  -h, --help            show this help message and exit
  --model {lr,cnn,gru,lstm,attention,resnet}
                        model name
  --train_data_path TRAIN_DATA_PATH
                        train data saved in numpy ndarray
  --train_label_path TRAIN_LABEL_PATH
                        train label saved in numpy ndarray
  --batch_size BATCH_SIZE
                        train batch size (default: 64)
  --epoch EPOCH         train epoch (default: 10)
  --lr LR               learning rate (default: 0.001)
  --lr_decay LR_DECAY   learning rate decay (default: 0.95)
  --model_saved MODEL_SAVED
                        model saved name (default: saved_model.h5)
```

```bash
python test5leaderC.py -h 
usage: test5leaderC.py [-h] [--model {lr,cnn,gru,lstm,attention}] [--test_data_path TEST_DATA_PATH] [--test_label_path TEST_LABEL_PATH]
                       [--model_dict_path MODEL_DICT_PATH]

PyTorch Implementation of aTSS Predict

optional arguments:
  -h, --help            show this help message and exit
  --model {lr,cnn,gru,lstm,attention}
                        model name
  --test_data_path TEST_DATA_PATH
                        test data saved in numpy ndarry
  --test_label_path TEST_LABEL_PATH
                        test label saved in numpy ndarray
  --model_dict_path MODEL_DICT_PATH
                        model saved name
```

#### 5'leaderL

```bash 
usage: train5leaderL.py [-h] [--model {cnn,gru,lstm,resnet} [{cnn,gru,lstm,resnet} ...]] [--train_data_path TRAIN_DATA_PATH]
                        [--train_label_path TRAIN_LABEL_PATH] [--batch_size BATCH_SIZE] [--epoch EPOCH] [--lr LR] [--lr_decay LR_DECAY]
                        [--model_saved_suffix MODEL_SAVED_SUFFIX]

PyTorch Implementation of aTSS Predict

optional arguments:
  -h, --help            show this help message and exit
  --model {cnn,gru,lstm,resnet} [{cnn,gru,lstm,resnet} ...]
                        model name
  --train_data_path TRAIN_DATA_PATH
                        train data saved in numpy ndarray
  --train_label_path TRAIN_LABEL_PATH
                        train label saved in numpy ndarray
  --batch_size BATCH_SIZE
                        train batch size(default: 64)
  --epoch EPOCH         train epoch(default: 10)
  --lr LR               learning rate (default: 0.001)
  --lr_decay LR_DECAY   learning rate decay (default: 0.95)
  --model_saved_suffix MODEL_SAVED_SUFFIX
                        model saved suffix (default: None)
```

```bash
python test5leaderL.py -h 
usage: test5leaderL.py [-h] [--test_data_path TEST_DATA_PATH] [--test_label_path TEST_LABEL_PATH] [--output OUTPUT]

PyTorch Implementation of aTSS Predict

optional arguments:
  -h, --help            show this help message and exit
  --test_data_path TEST_DATA_PATH
                        test data saved in numpy ndarray
  --test_label_path TEST_LABEL_PATH
                        test label saved in numpy ndarray
  --output OUTPUT       output path
```
### Examples

#### 5'leaderC

```bash
python train5leaderC.py --model resnet \
             --train_data_path ../../../../data/unique/class_data.npy \
             --train_label_path ../../../../data/unique/class_label.npy \
             --lr 0.001 --batch_size 64 \
             --model_save saved_model --epoch 100
```
    
#### 5'leaderL

```bash 
python train5leaderL.py --train_data_path ../../data/new_regress/regress_data_peak.npy \
                  --train_label_path ../../data/new_regress/regress_label_peak.npy \
                  --lr 0.001 --batch_size 256 \
                  --model_saved saved_model --epoch 300
```
    

