# Genermodel MAE in other species 
library(ggplot2)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/')

# version 20230321
# /home/zhusitao/AI/TSS_Predict/PlantModel/final_version/regress/github/data/random_select_singleton_new/tx436/get_mae.py
# df <- data.frame(MAE=c(21.10, 19.92, 20.16), Species=c('S.viridis', 'S.bicolor(Tx2783)', 'S.bicolor(Tx436)'))

# version 20230421
# /home/zhusitao/AI/TSS_Predict/PlantModel/TBF1_regression/TX2783_test/get_mae.py
# df <- data.frame(MAE=c(23.63, 22.05, 23.62), Species=c('S.viridis', 'S.bicolor(Tx2783)', 'S.bicolor(Tx436)'))
#ggplot(data = df, aes(x = Species, y = MAE, fill=Species)) +
#  geom_bar(width = 0.7,stat = 'identity') +
#  theme_classic() + ylim(0,25)

# FigS7b 见 TSS_FigS6_S7_species_cross_roc_pr_in_ResNet.R

# version 20230616 split_10
# /home/zhusitao/AI/TSS_Predict/PlantModel/TBF1_regression/tx436/split_10_fold/get_total.py
df <- read.csv('MAE_total.csv')
df

ggplot(data = df, aes(x = Species, y = MAE)) +
  theme_classic() + ylim(0,25) +
  geom_boxplot(outlier.shape = NA) + theme_classic() +
  geom_jitter(aes(color=Species, fill=Species), size=3, 
              shape=21, alpha=0.9, width= 0.3, height = 0.3) 

ggsave('general_model_MAE_in_new_species_total.pdf',width = 8, height = 6,units = 'in',dpi=300)
