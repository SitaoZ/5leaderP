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
