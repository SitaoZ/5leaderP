# copy model scripts
cp -r ../../final_version/class/github/current_new/ResNet/aTSS .
# copy saved model
cp ../../final_version/class/github/current_new/ResNet/saved_model.h5 .
# copy test scripts
cp ../../final_version/class/github/current_new/ResNet/test/ath/test5leaderC.py .

# predict 
python test5leaderC.py --model resnet --test_data_path test_class_data.npy --test_label_path test_class_label.npy --model_dict_path saved_model.h5
