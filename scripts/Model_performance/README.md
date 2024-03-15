# Model performance comparison in classification and regression

## Classification comparison 

The comparison input is the `hold-out` data that not used for model training. The data is feed into `TransPrise`, `TSSPlant` and `5leaderC` to evaluate the performance.

### 5leaderC
```bash
python test5leaderC.py --model resnet --test_data_path test_class_data.npy --test_label_path test_class_label.npy --model_dict_path saved_model.h5
Namespace(model='resnet', model_dict_path='saved_model.h5', test_data_path='test_class_data.npy', test_label_path='test_class_label.npy')

Test set: Average loss: 0.1290, Accuracy: 2091/2176 (96%)

TP: 1054 ; TN: 1041 ; FP: 33 ; FN: 48
Accuracy: 0.9627757352941176
Sensetivity: 0.956442831215971
Specificity: 0.9692737430167597
AUC: 0.993297694728055
```

### TransPrise

```bash
# step1
pip install -r requires.txt
# step2
conda activate TP
# step3
python TransPrise_comparison.py
# step4
cp PR_Curve_data.csv PR_Curve_data_TransPrise.csv
cp ROC_Curve_data.csv ROC_Curve_data_TransPrise.csv
```


### TSSPlant

```bash
# setp1
cp ../../final_version/class/github/current_new/ResNet/predict_result.csv .

# step2
less predict_result.csv | sed '1d' |awk -F',' '{print ">seq"NR"-"$2"\n"$3}' > query.seq

# step3
TSSPlant -i:query.seq -o:query.res -t:n

# step4
python TSSPlant_compare.py

# step5
cp ROC_Curve_data.csv ROC_Curve_data_TSSPlant.csv
cp PR_Curve_data.csv PR_Curve_data_TSSPlant.csv
```


## Regression model comparison
The `hold-out` data is used for model performance comparison. each dir contains the codes and models for prediction.

### 5leaderL

```bash
# step1
cp /home/zhusitao/AI/TSS_Predict/ath/regression/predict_peak.csv .

# step2
# Regression models including attention.pt, cnn.pt, gru.pt, lstm.pt and resnet.pt should exist in current dir
# scaler.joblib also exists
python predict5leaderL.py --predict_data_path predict_peak.csv --output predict_again.csv

# step3
# calculate the MAE from predict_again.csv
python get_mae.py
```

### TransPrise

```bash
# step1
pip install -r requires.txt

# step2 
conda activate TP

# step3
python TransPrise_compare.py
```


### TSSFinder

```bash
# step1
python get_start_codon.py
# step2
python get_data.py
# step3
cp /home/zhusitao/AI/TSS_Predict/ath/regression/predict_peak.csv .
# step4
tssfinder --model /home/zhusitao/AI/TSS_Predict/rice/TSSFinder/athaliana/athaliana.0 \
          --start input_predict.bed \
          --genome TAIR10.fa \
          --output output_athaliana.model_0
# step5 
cd output_athaliana.model_0
python get_mae.py
```

### TSSPlant

```bash
# step1
cp /home/zhusitao/AI/TSS_Predict/ath/regression/predict_peak.csv .
less predict_peak.csv | sed '1d' |awk -F',' '{print ">"$6"_"$4"\n"$5}' > query.seq

# step2
TSSPlant -i:query.seq -o:query.res -t:n -b:512 -p:y 

# step3
python TSSPlant_compare.py
```
