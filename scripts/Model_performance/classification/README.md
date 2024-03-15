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
