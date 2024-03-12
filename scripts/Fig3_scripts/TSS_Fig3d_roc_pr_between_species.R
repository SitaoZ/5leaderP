# species transcript/gene
# 数据集来源 115.156.67.100 /home/zhusitao/AI/TSS_Predict
library(ggplot2)
getwd()
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/')


# /home/zhusitao/AI/TSS_Predict/species_roc_merge.csv
# roc <- read.csv('final_version/20230322/ResNet_species_roc_merge.csv')
# /home/zhusitao/AI/TSS_Predict/20230421
roc <- read.csv('final_version/20230421/ResNet_species_roc_merge.csv')
head(roc)
dim(roc)
## auc calc
### roc calculate 

simple_auc <- function(TPR, FPR){
  # inputs already sorted, best scores first 
  dFPR <- c(diff(FPR), 0)
  dTPR <- c(diff(TPR), 0)
  sum(TPR * dFPR) + sum(dTPR * dFPR)/2
}
simple_auc(roc$tpr, roc$fpr)

ath <- roc[roc$Species == 'Arabidopsis', ]
round(simple_auc(ath$tpr, ath$fpr), 4)

osa <- roc[roc$Species == 'Rice', ]
round(simple_auc(osa$tpr, osa$fpr),4)

gab <- roc[roc$Species == 'Cotton', ]
round(simple_auc(gab$tpr, gab$fpr),4)

zma <- roc[roc$Species == 'Maize', ]
round(simple_auc(zma$tpr, zma$fpr), 4)

gmx <- roc[roc$Species == 'Soybean', ]
round(simple_auc(gmx$tpr, gmx$fpr), 4)

# current version 
# species_performance <- data.frame(ModelType = c('ath', 'osa', 'gab', 'zma', 'gmx'),
#                          auc_value = c(0.9934, 0.9941, 0.9903, 0.9914, 0.9926))
# current_new 
species_performance <- data.frame(ModelType = c('ath', 'osa', 'gab', 'zma', 'gmx'),
                          auc_value = c(0.9765, 0.9836, 0.9675, 0.9782, 0.9772))
species_performance
##
ggplot(roc, aes(fpr,tpr, color=Species)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  annotate("text", x = 0.8, y=c(0.1, 0.14,0.18,0.22, 0.26), 
           label = c('AUC = 0.9765', 'AUC = 0.9836', 
                     'AUC = 0.9675', 'AUC = 0.9782', 'AUC = 0.9772'))

#ggsave('final_version/20230322/Species_ROC.pdf',width = 8, height = 6,units = 'in',dpi=300)
ggsave('final_version/20230421/Species_ROC.pdf',width = 8, height = 6,units = 'in',dpi=300)

# pr <- read.csv('final_version/20230322/ResNet_pr_merge_average.csv')
pr <- read.csv('final_version/20230421/ResNet_pr_merge_average.csv')
ggplot(pr,aes(recall,precision, color=Species)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "PR curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0))

# ggsave('final_version/20230322/Species_PR.pdf',width = 8, height = 6,units = 'in',dpi=300)
ggsave('final_version/20230421/Species_PR.pdf',width = 8, height = 6,units = 'in',dpi=300)
