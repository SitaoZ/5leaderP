# step1
cp /home/zhusitao/AI/TSS_Predict/ath/regression/predict_peak.csv .

# step2
python predict5leaderL.py --predict_data_path predict_peak.csv --output predict_again.csv

# step3
python get_mae.py 
