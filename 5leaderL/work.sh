# train
python train5leaderL.py --train_data_path ./data/regress_data_peak.npy \
                  --train_label_path ./data/regress_label_peak.npy \
                  --lr 0.001 --batch_size 256 \
                  --model_saved saved_model --epoch 200

# predict 
python predict5leaderL.py --predict_data_path ./data/TBF1.csv --output TBF1_pred.csv
