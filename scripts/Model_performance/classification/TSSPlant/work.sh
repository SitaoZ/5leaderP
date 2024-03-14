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
