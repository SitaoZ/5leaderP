# TSS general model performance 
library(ggplot2)
library(pROC)
# working diar setting 
getwd()
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/general_model_performance/')

#### color brewer
library(RColorBrewer)
?RColorBrewer
display.brewer.all(n=NULL, type="all", select=NULL, exact.n=TRUE, 
                   colorblindFriendly=FALSE)
mypalette <- brewer.pal(7,"Set2")

### roc calculate 

simple_auc <- function(TPR, FPR){
  # inputs already sorted, best scores first 
  dFPR <- c(diff(FPR), 0)
  dTPR <- c(diff(TPR), 0)
  sum(TPR * dFPR) + sum(dTPR * dFPR)/2
}
#simple_auc(roc$tpr, roc$fpr)

# roc <- read.csv('another_512_version/roc_merge.csv')
# roc <- read.csv('final_version/roc_merge.csv') 
# roc <- read.csv('20230323/roc_merge.csv') # 20230323 version
roc <- read.csv('20230421/roc_merge.csv') # 20230421 version
roc

LR <- roc[roc$ModelType == 'LR', ]
round(simple_auc(LR$tpr, LR$fpr), 4)

CNN <- roc[roc$ModelType == 'CNN', ]
round(simple_auc(CNN$tpr, CNN$fpr), 4)

Attention <- roc[roc$ModelType == 'Attention', ]
round(simple_auc(Attention$tpr, Attention$fpr),4)

LSTM <- roc[roc$ModelType == 'LSTM', ]
round(simple_auc(LSTM$tpr, LSTM$fpr),4)

GRU <- roc[roc$ModelType == 'GRU', ]
round(simple_auc(GRU$tpr, GRU$fpr), 4)

ResNet <- roc[roc$ModelType == 'ResNet', ]
round(simple_auc(ResNet$tpr, ResNet$fpr), 4)

# final_version
label_model <- data.frame(ModelType = c('LR', 'CNN', 'Attention', 'LSTM', 'GRU', 'ResNet'),
                          auc_value = c(0.9012, 0.9737, 0.9462, 0.9727, 0.9746, 0.979))
label_model


roc$ModelType <- factor(roc$ModelType, levels = c("ResNet","Attention","GRU","CNN","LSTM","LR"))
# roc curve 
mypalette <- brewer.pal(7,"Set1")
ggplot(roc, aes(fpr,tpr, color=ModelType)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  annotate("text", x = 0.8, y=c(0.1, 0.14,0.18,0.22, 0.26, 0.30), 
           label = c('AUC = 0.9012', 'AUC = 0.9737', 'AUC = 0.9462',
                     'AUC = 0.9727', 'AUC = 0.9746', 'AUC = 0.979')) +
  scale_colour_manual(values=mypalette)

# save figure
ggsave('20230421/general_ROC.pdf',width = 8, height = 6,units = 'in',dpi=300)

# pr curve
# pr <- read.csv('final_version/pr_merge.csv')
# pr <- read.csv('20230323/pr_merge.csv') # 20230323
pr <- read.csv('20230421/pr_merge.csv') # 20230421
head(pr)
dim(pr)
pr$ModelType <- factor(pr$ModelType, levels = c("ResNet","Attention","GRU","CNN","LSTM","LR"))
ggplot(pr,aes(recall,precision, color=ModelType)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "PR curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  scale_colour_manual(values=mypalette)
# save figure
ggsave('20230421/general_PR.pdf',width = 8, height = 6,units = 'in',dpi=300)
