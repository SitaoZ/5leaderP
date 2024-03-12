# 10X cross fold validation 
library(ggplot2)
library(RColorBrewer)

display.brewer.all(n=NULL, type="all", select=NULL, exact.n=TRUE, 
                   colorblindFriendly=FALSE)
mypalette <- brewer.pal(12,"Paired")




# 20230312(current) 版本数据 /home/zhusitao/AI/TSS_Predict/ath/union_tss/final_version/class/github/current/ResNet/tenFoldCrossValidROC.csv
# 20230322(current_new) 版本数据/home/zhusitao/AI/TSS_Predict/ath/union_tss/final_version/class/github/current_new/ResNet/tenFoldCrossValidROC.csv
# ROC
# 20230421(classification) /home/zhusitao/AI/TSS_Predict/ath/classification/ResNet/tenFoldCrossValidROC.csv

setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/roc_pr/ath/20230421/')
tenFoldROC <- read.csv('tenFoldCrossValidROC.csv')
head(tenFoldROC)
  
ggplot(tenFoldROC, aes(fpr,tpr, color=fold)) + 
  geom_line(size = 0.6, alpha = 1) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0))+
  scale_colour_manual(values=mypalette)
ggsave('tenFold_ROC.pdf',width = 8, height = 6,units = 'in',dpi=300)

# PR
tenFoldPR <- read.csv('tenFoldCrossValidPR.csv')
head(tenFoldPR)
ggplot(tenFoldPR, aes(recall,precision, color=fold)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "PR curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  scale_colour_manual(values=mypalette)
ggsave('tenFold_PR.pdf',width = 8, height = 6,units = 'in',dpi=300)

## gerneral model #######################################################################
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/roc_pr/plant/ResNet/')

# roc curve 

simple_auc <- function(TPR, FPR){
  # inputs already sorted, best scores first 
  dFPR <- c(diff(FPR), 0)
  dTPR <- c(diff(TPR), 0)
  sum(TPR * dFPR) + sum(dTPR * dFPR)/2
}

# ROC
tenFoldROC <- read.csv('final_version/tenFoldCrossValidROC.csv')
head(tenFoldROC)
library(tidyverse)
fold1 <- filter(tenFoldROC, fold=="fold1")
fold1_auc <- simple_auc(fold1$tpr, fold1$fpr)
fold1_auc

# R loop 
auc_values <- c()
for (x in 1:10){
  y <- paste('fold',x, sep="")
  z <- filter(tenFoldROC, fold==y)
  auc_value <- round(simple_auc(z$tpr, z$fpr), 4)
  print(auc_value)
  auc_values <- c(auc_values, auc_value)
}
print(auc_values)


# general model 
# ggplot(tenFoldROC, aes(fpr,tpr, color=fold, linetype=fold)) + 
# /home/zhusitao/AI/TSS_Predict/PlantModel/another_512_class/ResNet/tenFoldCrossValidROC.csv
ggplot(tenFoldROC, aes(fpr,tpr, color=fold)) + 
  geom_line(size = 0.6, alpha = 1) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0))+
  scale_colour_manual(values=mypalette) + 
  annotate("text", x = 0.8, y=c(0.1, 0.14, 0.18, 0.22, 0.26, 0.3, 0.34, 0.38, 0.42, 0.46), 
           label = c('fold9 AUC = 0.9808', 'fold8 AUC = 0.9813', 'fold7 AUC = 0.9817',
                     'fold6 AUC = 0.9815', 'fold5 AUC = 0.9799', 'fold4 AUC = 0.9805',
                     'fold3 AUC = 0.9823', 'fold2 AUC = 0.9814', 'fold10 AUC = 0.9795',
                     'fold1 AUC = 0.9814'))
  
ggsave('final_version/tenFold_ROC.pdf',width = 8, height = 6,units = 'in',dpi=300)

# PR
# tenFoldPR <- read.csv('tenFoldCrossValidPR.csv')
tenFoldPR <- read.csv('final_version/tenFoldCrossValidPR_average.csv')
head(tenFoldPR)
# ggplot(tenFoldPR, aes(recall,precision, color=fold, linetype=fold)) + 
ggplot(tenFoldPR, aes(recall,precision, color=fold)) + 
  geom_line(size = 0.6, alpha = 1) +
  labs(title= "PR curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  scale_colour_manual(values=mypalette)
ggsave('final_version/tenFold_PR.pdf',width = 8, height = 6,units = 'in',dpi=300)

