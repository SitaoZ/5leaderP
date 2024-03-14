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


# check
# 1	4105259	4105260	AT1G12110_1	1	+ Cross validation/TSS prediction 和我们预测的一样
#  less output_athaliana.model_0/out.tss.bed | grep AT1G12110
# Chr1	4105259	4105260	AT1G12110.1	1	+
# 1	22462189	22462190	AT1G60989_1	1	+ 预测也一致

# less output_athaliana.model_0/out.tss.bed | grep AT1G60989
# Chr1	22462189	22462190	AT1G60989.1	1	+


# 2	14146414	14146415	AT2G33380_1	1	-
# Chr2	14146414	14146415	AT2G33380.2	1	-
# cat predict_peak.csv | cut -d , -f 6 | sed '1d' > ts_id_predict
