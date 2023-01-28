python trainTSARC.py --model resnet \
             --train_data_path ../../data/class_data.npy \
             --train_label_path ../../data/class_label.npy \
             --lr 0.001 --batch_size 256 \
             --model_save saved_model --epoch 100
