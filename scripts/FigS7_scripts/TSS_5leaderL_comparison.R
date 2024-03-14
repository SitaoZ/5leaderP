library(ggplot2)
library(gg.gap)
library(ggpubr)
library(ggpmisc)
library(ggsci)
library(RColorBrewer)
display.brewer.all( type = 'all')
mypalette <- brewer.pal(n = 8, 'Paired')

# /home/zhusitao/AI/TSS_Predict/ath/TSARC_TSSPlant_TransPrise/regression_compare/MAE_comparison.csv
library(ggsci)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/')

df <- read.csv('ath_MAE_comparison.csv')
head(df)
ggplot(data = df, aes(x = Model, y = MAE, color = Model)) + 
  geom_boxplot(outlier.shape = NA) + theme_classic() + scale_color_npg() +
  geom_jitter(width = 0.3) 
ggsave('ath_leaerL_TSSFinder_TSSPlant_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)


# /home/zhusitao/AI/TSS_Predict/rice/TSARC_TSSPlant_TransPrise/regression_compare/MAE_comparison.csv

df <- read.csv('rice_MAE_comparison.csv')
head(df)
ggplot(data = df, aes(x = Model, y = MAE, color = Model)) + 
  geom_boxplot(outlier.shape = NA) + theme_classic() + scale_color_npg() +
  geom_jitter(width = 0.3) 
ggsave('rice_leaerL_TSSFinder_TSSPlant_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)
