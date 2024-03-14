# step1
cp /home/zhusitao/AI/TSS_Predict/ath/regression/predict_peak.csv .
less predict_peak.csv | sed '1d' |awk -F',' '{print ">"$6"_"$4"\n"$5}' > query.seq

# step2
TSSPlant -i:query.seq -o:query.res -t:n -b:512 -p:y 

# step3
python TSSPlant_compare.py

