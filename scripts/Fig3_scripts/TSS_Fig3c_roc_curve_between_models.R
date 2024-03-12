library(ggplot2)
library(pROC)
# working diar setting 
getwd()
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/roc_pr')

#### color brewer
library(RColorBrewer)
?RColorBrewer
display.brewer.all(n=NULL, type="all", select=NULL, exact.n=TRUE, 
                   colorblindFriendly=FALSE)
mypalette <- brewer.pal(7,"Set1")

### roc calculate 

simple_auc <- function(TPR, FPR){
  # inputs already sorted, best scores first 
  dFPR <- c(diff(FPR), 0)
  dTPR <- c(diff(TPR), 0)
  sum(TPR * dFPR) + sum(dTPR * dFPR)/2
}

#################################### ath #################################
# current /home/zhusitao/AI/TSS_Predict/ath/union_tss/final_version/class/github/current
# current_new /home/zhusitao/AI/TSS_Predict/ath/union_tss/final_version/class/github/current_new
# ath_roc <- read.csv('ath/20230322/roc_merge.csv')
# version20230421 /home/zhusitao/AI/TSS_Predict/ath/classification
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/roc_pr')
ath_roc <- read.csv('ath/20230421/roc_merge.csv')
ath_roc
simple_auc(ath_roc$tpr, ath_roc$fpr)

LR <- ath_roc[ath_roc$ModelType == 'LR', ]
round(simple_auc(LR$tpr, LR$fpr), 4)

ResNet <- ath_roc[ath_roc$ModelType == 'ResNet', ]
round(simple_auc(ResNet$tpr, ResNet$fpr),4)

Attention <- ath_roc[ath_roc$ModelType == 'Attention', ]
round(simple_auc(Attention$tpr, Attention$fpr),4)

LSTM <- ath_roc[ath_roc$ModelType == 'LSTM', ]
round(simple_auc(LSTM$tpr, LSTM$fpr),4)

CNN <- ath_roc[ath_roc$ModelType == 'CNN', ]
round(simple_auc(CNN$tpr, CNN$fpr), 4)

GRU <- ath_roc[ath_roc$ModelType == 'GRU', ]
round(simple_auc(GRU$tpr, GRU$fpr), 4)

# current version 
#label_model <- data.frame(ModelType = c('LR', 'CNN', 'Attention', 'LSTM', 'GRU', 'ResNet'),
#                          auc_value = c(0.9408, 0.9891, 0.9811, 0.9901, 0.9896, 0.9934))
# current_new version 
#label_model <- data.frame(ModelType = c('LR', 'CNN', 'Attention', 'LSTM', 'GRU', 'ResNet'),
#                          auc_value = c(0.9416, 0.9883, 0.9814, 0.9904, 0.9898, 0.9935))

label_model <- data.frame(ModelType = c('LR', 'CNN', 'Attention', 'LSTM', 'GRU', 'ResNet'),
                          auc_value = c(0.8719, 0.9676, 0.9275, 0.972, 0.9689, 0.9765))
label_model
ath_roc$ModelType <- factor(ath_roc$ModelType, levels = c("Attention","CNN", "GRU", "LR","LSTM", "ResNet"))
# roc curve 
ggplot(ath_roc, aes(fpr,tpr, color=ModelType)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  annotate("text", x = 0.8, y=c(0.1, 0.14,0.18,0.22, 0.26, 0.30), 
           label = c('AUC = 0.8719', 'AUC = 0.9676', 
                     'AUC = 0.9275', 'AUC = 0.972', 
                     'AUC = 0.9689', 'AUC = 0.9765')) +
  scale_colour_manual(values=mypalette)

# save figure
# ggsave('ath/20230322/ath_ROC.pdf',width = 8, height = 6,units = 'in',dpi=300)
ggsave('ath/20230421/ath_ROC.pdf',width = 8, height = 6,units = 'in',dpi=300)

# pr curve
# ath_pr <- read.csv('ath/20230322/pr_merge.csv')
ath_pr <- read.csv('ath/20230421/pr_merge.csv')
head(ath_pr)
dim(ath_pr)
ath_pr$ModelType <- factor(ath_pr$ModelType, levels = c("Attention","CNN", "GRU", "LR","LSTM", "ResNet"))
ggplot(ath_pr,aes(recall,precision, color=ModelType)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "PR curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  scale_colour_manual(values=mypalette)
# save figure
# ggsave('ath/20220322/ath_PR.pdf',width = 8, height = 6,units = 'in',dpi=300)
ggsave('ath/20230421/ath_PR.pdf',width = 8, height = 6,units = 'in',dpi=300)


################################### rice ##################################
# read data 
rice_roc <- read.csv('rice/roc_merge.csv')
rice_roc
dim(rice_roc)
head(rice_roc)
# roc curve 
lr <- filter(rice_roc, ModelType=="LR")
lr_auc <- simple_auc(lr$tpr, lr$fpr)
lr_auc
cnn <- filter(rice_roc, ModelType=="CNN")
cnn_auc <- simple_auc(cnn$tpr, cnn$fpr)
cnn_auc
lstm <- filter(rice_roc, ModelType=="LSTM")
lstm_auc <- simple_auc(lstm$tpr, lstm$fpr)
lstm_auc
gru <- filter(rice_roc, ModelType=="GRU")
gru_auc <- simple_auc(gru$tpr, gru$fpr)
gru_auc
attention <- filter(rice_roc,ModelType=="Attention")
attention_auc <- simple_auc(attention$tpr, attention$fpr)
attention_auc
ggplot(rice_roc, aes(fpr,tpr, color=ModelType)) + 
  geom_line(size = 1, alpha = 0.9) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  annotate("text", x = 0.8, y=c(0.1, 0.14,0.18,0.22, 0.26), 
           label = c('AUC = 0.8480', 'AUC = 0.9674', 
                     'AUC = 0.9588', 'AUC = 0.9722', 'AUC = 0.9790')) +
  scale_colour_manual(values=mypalette) +
  labs(title = 'Rice Receiver-operating Characteristic (ROC) Curve') +
  theme(plot.title = element_text(hjust = 0.5))
# save figure
ggsave('rice/rice_ROC.pdf',width = 8, height = 6,units = 'in',dpi=300)

# pr curve
rice_pr <- read.csv('rice/pr_merge.csv')
head(rice_pr)
ggplot(rice_pr,aes(recall,precision, color=ModelType)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "PR curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  scale_colour_manual(values=mypalette) + 
  labs(title = 'Rice Precision-Recall (PR) Curve') +
  theme(plot.title = element_text(hjust = 0.5))
# save figure
ggsave('rice/rice_PR.pdf',width = 8, height = 6,units = 'in',dpi=300)

# ---------------------- cotton -----------------
# read data 
library(dplyr)
cotton_roc <- read.csv('cotton/roc_merge.csv')
cotton_roc
dim(cotton_roc)
head(cotton_roc)
# roc curve 
lr <- filter(cotton_roc, ModelType=="LR")
lr_auc <- simple_auc(lr$tpr, lr$fpr)
lr_auc
cnn <- filter(cotton_roc, ModelType=="CNN")
cnn_auc <- simple_auc(cnn$tpr, cnn$fpr)
cnn_auc
lstm <- filter(cotton_roc, ModelType=="LSTM")
lstm_auc <- simple_auc(lstm$tpr, lstm$fpr)
lstm_auc
gru <- filter(cotton_roc, ModelType=="GRU")
gru_auc <- simple_auc(gru$tpr, gru$fpr)
gru_auc
attention <- filter(cotton_roc,ModelType=="Attention")
attention_auc <- simple_auc(attention$tpr, attention$fpr)
attention_auc
ggplot(cotton_roc, aes(fpr,tpr, color=ModelType)) + 
  geom_line(size = 1, alpha = 0.9) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  annotate("text", x = 0.8, y=c(0.1, 0.14,0.18,0.22, 0.26), 
           label = c('AUC = 0.7132', 'AUC = 0.9312', 
                     'AUC = 0.9181', 'AUC = 0.9266', 'AUC = 0.9342')) +
  scale_colour_manual(values=mypalette) +
  labs(title = 'Cotton Receiver-operating Characteristic (ROC) Curve') +
  theme(plot.title = element_text(hjust = 0.5))
# save figure
ggsave('cotton/cotton_ROC.pdf',width = 8, height = 6,units = 'in',dpi=300)

# pr curve
cotton_pr <- read.csv('cotton/pr_merge.csv')
head(cotton_pr)
ggplot(cotton_pr,aes(recall,precision, color=ModelType)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "PR curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  scale_colour_manual(values=mypalette) + 
  labs(title = 'Cotton Precision-Recall (PR) Curve') +
  theme(plot.title = element_text(hjust = 0.5))
# save figure
ggsave('cotton/cotton_PR.pdf',width = 8, height = 6,units = 'in',dpi=300)

# ---------------------- maize -----------------------------
# read data 
maize_roc <- read.csv('maize/roc_merge.csv')
maize_roc
dim(maize_roc)
head(maize_roc)
# roc curve 
lr <- filter(maize_roc, ModelType=="LR")
lr_auc <- simple_auc(lr$tpr, lr$fpr)
lr_auc
cnn <- filter(maize_roc, ModelType=="CNN")
cnn_auc <- simple_auc(cnn$tpr, cnn$fpr)
cnn_auc
lstm <- filter(maize_roc, ModelType=="LSTM")
lstm_auc <- simple_auc(lstm$tpr, lstm$fpr)
lstm_auc
gru <- filter(maize_roc, ModelType=="GRU")
gru_auc <- simple_auc(gru$tpr, gru$fpr)
gru_auc
attention <- filter(maize_roc,ModelType=="Attention")
attention_auc <- simple_auc(attention$tpr, attention$fpr)
attention_auc
ggplot(maize_roc, aes(fpr,tpr, color=ModelType)) + 
  geom_line(size = 1, alpha = 0.9) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  annotate("text", x = 0.8, y=c(0.1, 0.14,0.18,0.22, 0.26), 
           label = c('AUC = 0.7392', 'AUC = 0.9483', 
                     'AUC = 0.9322', 'AUC = 0.9515', 'AUC = 0.9594')) +
  scale_colour_manual(values=mypalette) +
  labs(title = 'Maize Receiver-operating Characteristic (ROC) Curve') +
  theme(plot.title = element_text(hjust = 0.5))
# save figure
ggsave('maize/maize_ROC.pdf',width = 8, height = 6,units = 'in',dpi=300)

# pr curve
maize_pr <- read.csv('maize/pr_merge.csv')
head(maize_pr)
ggplot(maize_pr,aes(recall,precision, color=ModelType)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "PR curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  scale_colour_manual(values=mypalette) + 
  labs(title = 'Maize Precision-Recall (PR) Curve') +
  theme(plot.title = element_text(hjust = 0.5))
# save figure
ggsave('maize/maize_PR.pdf',width = 8, height = 6,units = 'in',dpi=300)

#  soybean 
# ---------------------- soybean -----------------------------
# read data 
soybean_roc <- read.csv('soybean/roc_merge.csv')
soybean_roc
dim(soybean_roc)
head(soybean_roc)
# roc curve 
lr <- filter(soybean_roc, ModelType=="LR")
lr_auc <- simple_auc(lr$tpr, lr$fpr)
lr_auc
cnn <- filter(soybean_roc, ModelType=="CNN")
cnn_auc <- simple_auc(cnn$tpr, cnn$fpr)
cnn_auc
lstm <- filter(soybean_roc, ModelType=="LSTM")
lstm_auc <- simple_auc(lstm$tpr, lstm$fpr)
lstm_auc
gru <- filter(soybean_roc, ModelType=="GRU")
gru_auc <- simple_auc(gru$tpr, gru$fpr)
gru_auc
attention <- filter(soybean_roc,ModelType=="Attention")
attention_auc <- simple_auc(attention$tpr, attention$fpr)
attention_auc
ggplot(soybean_roc, aes(fpr,tpr, color=ModelType)) + 
  geom_line(size = 1, alpha = 0.9) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  annotate("text", x = 0.8, y=c(0.1, 0.14,0.18,0.22, 0.26), 
           label = c('AUC = 0.8547', 'AUC = 0.9608', 
                     'AUC = 0.9502', 'AUC = 0.9597', 'AUC = 0.9654')) +
  scale_colour_manual(values=mypalette) +
  labs(title = 'Soybean Receiver-operating Characteristic (ROC) Curve') +
  theme(plot.title = element_text(hjust = 0.5))
# save figure
ggsave('soybean/soybean_ROC.pdf',width = 8, height = 6,units = 'in',dpi=300)

# pr curve
soybean_pr <- read.csv('soybean/pr_merge.csv')
head(soybean_pr)
ggplot(soybean_pr,aes(recall,precision, color=ModelType)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "PR curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  scale_colour_manual(values=mypalette) + 
  labs(title = 'Soybean Precision-Recall (PR) Curve') +
  theme(plot.title = element_text(hjust = 0.5))
# save figure
ggsave('soybean/soybean_PR.pdf',width = 8, height = 6,units = 'in',dpi=300)

##################### total model (PlantModel) #############
library(ggplot2)
library(pROC)
# working diar setting 
getwd()
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/roc_pr')

plant_roc <- read.csv('plant/roc_merge.csv')
plant_roc
dim(plant_roc)
head(plant_roc)
# roc curve 
auc <- round(auc(plant_roc$fpr, plant_roc$tpr),4)

ggplot(plant_roc, aes(fpr,tpr, color=ModelType)) + 
  geom_line(size = 1, alpha = 0.9) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  scale_colour_manual(values=mypalette)
# save figure
ggsave('plant/plant_ROC.pdf',width = 8, height = 6,units = 'in',dpi=300)

# pr curve
plant_pr <- read.csv('plant/pr_merge.csv')
head(plant_pr)
ggplot(plant_pr,aes(recall,precision, color=ModelType)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "PR curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  scale_colour_manual(values=mypalette)
# save figure
ggsave('plant/plant_PR.pdf',width = 8, height = 6,units = 'in',dpi=300)
