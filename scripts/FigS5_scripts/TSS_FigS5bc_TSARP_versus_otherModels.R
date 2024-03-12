# Comparing the model performance between own and TransPrise
library(ggplot2)
getwd()

#   ath 
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/TSARP_versus_other_software/')
# setwd('/Users/zhusitao/Downloads/') # test
# TSARP
TSARP_roc <- read.csv('ath/ROC_Curve_fold10_data.csv')
TSARP_roc$Type <- 'TSARC'

# TransPrise
tr_roc <- read.csv('ath/ROC_Curve_data_TransPrise.csv')
tr_roc$Type <- 'TransPrise'

# TSSPlant
tp_roc <- read.csv('ath/ROC_Curve_data_TSSPlant.csv')
tp_roc$Type <- 'TSSPlant'

# one figure 
total_roc_merge <- rbind(TSARP_roc, tp_roc, tr_roc)
head(total_roc_merge)
ggplot(total_roc_merge, aes(fpr,tpr, color=Type)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0))
ggsave('ath/roc_TSARC_TSSPlant_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)

# PR 
# PR 数据减少，便于画图
# /home/zhusitao/AI/TSS_Predict/ath/final_version/class/ResNet/PR_inter.py


TSARP_pr <- read.csv('ath/PR_Curve_fold10_data.csv')
TSARP_pr$Type <- 'TSARC'
head(TSARP_pr)

tr_pr <- read.csv('ath/PR_Curve_data_TransPrise.csv')

tr_pr$Type <- 'TransPrise'
head(tr_pr)

tp_pr <- read.csv('ath/PR_Curve_data_TSSPlant.csv')
# tp_pr <- read.csv('ath/PR_Curve_data_TSSPlant_new.csv')
tp_pr$Type <- 'TSSPlant'
head(tp_pr)

# one figure 
total_pr_merge <- rbind(TSARP_pr, tp_pr, tr_pr)
head(total_pr_merge)
ggplot(total_pr_merge, aes(recall,precision, color=Type)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "P-R curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) 
ggsave('ath/pr_TSARC_TSSPlant_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)


#  rice TransPrise versus TSARP
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/TSARP_versus_other_software/')
# TSARP
# ath rice cotton maize soybean
TSARP_roc <- read.csv('rice/ROC_Curve_fold10_data.csv')
TSARP_roc$Type <- 'TSARC'
head(TSARP_roc)

# TransPrise
# /home/zhusitao/AI/TSS_Predict/rice/TransPrise-master
tr_roc <- read.csv('rice/ROC_Curve_data_TransPrise.csv')
tr_roc$Type <- 'TransPrise'
head(tr_roc)

# TSSPlant
# /home/zhusitao/AI/TSS_Predict/rice/TSSPlant/TSSPlant-master/TSSPlant/performance_vs_our_model
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/TSARP_versus_other_software/')

# tp_roc <- read.csv('TSARP_versus_TSSPlant/ROC_Curve_data_TSSPlant.csv')
tp_roc <- read.csv('rice/ROC_Curve_data_TSSPlant.csv')
tp_roc$Type <- 'TSSPlant'
head(tp_roc)


# TSARP vs TransPrise
#roc_merge <- rbind(TSARP_roc, tr_roc)
#roc_merge
#head(roc_merge)
#ggplot(roc_merge, aes(fpr,tpr, color=Type)) + 
#  geom_line(size = 1, alpha = 1) +
#  labs(title= "ROC curve", 
#       x = "False Positive Rate (1-Specificity)", 
#       y = "True Positive Rate (Sensitivity)") +
#  theme_classic() +
#  geom_abline(linetype = 'dashed') +
#  scale_x_continuous(expand = c(0, 0)) +
#  scale_y_continuous(expand = c(0, 0))
#ggsave('roc_curve_TSARC_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)

# TSARP vs TSSPlant
#roc_merge <- rbind(TSARP_roc, tp_roc)
#roc_merge
#head(roc_merge)
#ggplot(roc_merge, aes(fpr,tpr, color=Type)) + 
#  geom_line(size = 1, alpha = 1) +
##  labs(title= "ROC curve", 
#       x = "False Positive Rate (1-Specificity)", 
#       y = "True Positive Rate (Sensitivity)") +
#  theme_classic() +
##  geom_abline(linetype = 'dashed') +
#  scale_x_continuous(expand = c(0, 0)) +
#  scale_y_continuous(expand = c(0, 0))
#ggsave('roc_curve_TSARC_TSSPlant.pdf',width = 8, height = 6,units = 'in',dpi=300)



# one figure 
total_roc_merge <- rbind(TSARP_roc, tp_roc, tr_roc)
total_roc_merge
head(total_roc_merge)
ggplot(total_roc_merge, aes(fpr,tpr, color=Type)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0))
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/TSARP_versus_other_software/')
ggsave('rice/roc_TSARC_TSSPlant_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)
# PR 
# own_pr <- read.csv('PR_Curve_data_own.csv')
# own_pr$Type <- 'TSS_Predict'
# head(own_pr)

# TSARP_pr <- read.csv('../TSARP_versus_TransPrise/PR_Curve_fold10_data.csv')
# TSARP_pr <- read.csv('TSARP_versus_TransPrise/PR_Curve_mean_data.csv')
TSARP_pr <- read.csv('rice/PR_Curve_fold10_data.csv')
TSARP_pr$Type <- 'TSARC'
head(TSARP_pr)

# tr_pr <- read.csv('TSARP_versus_TransPrise/PR_Curve_data_TransPrise.csv')
tr_pr <- read.csv('rice/PR_Curve_data_TransPrise.csv')
tr_pr$Type <- 'TransPrise'
head(tr_pr)

# tp_pr <- read.csv('TSARP_versus_TSSPlant/PR_Curve_data_TSSPlant.csv')
tp_pr <- read.csv('rice/PR_Curve_data_TSSPlant.csv')
tp_pr$Type <- 'TSSPlant'
head(tp_pr)

# Own vs TransPrise 
# pr_merge <- rbind(own_pr, tr_pr)
#pr_merge <- rbind(TSARP_pr, tr_pr)
#head(pr_merge)
#ggplot(pr_merge,aes(recall,precision, color=Type)) + 
#  geom_line(size = 1, alpha = 1) +
#  labs(title= "PR curve", 
#       x = "Recall", 
#       y = "Precision") +
#  theme_classic() +
#  scale_x_continuous(expand = c(0, 0)) +
#  scale_y_continuous(expand = c(0, 0))
#ggsave('pr_curve_TSARC_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)


# Own vs TSSPlant 

#pr_merge <- rbind(TSARP_pr, tp_pr)
#head(pr_merge)
#ggplot(pr_merge,aes(recall,precision, color=Type)) + 
#  geom_line(size = 1, alpha = 1) +
#  labs(title= "PR curve", 
#       x = "Recall", 
#       y = "Precision") +
#  theme_classic() +
#  scale_x_continuous(expand = c(0, 0)) +
#  scale_y_continuous(expand = c(0, 0))
#ggsave('pr_curve_TSARC_TSSPlant.pdf',width = 8, height = 6,units = 'in',dpi=300)

# one figure 
total_pr_merge <- rbind(TSARP_pr, tp_pr, tr_pr)
total_pr_merge
head(total_pr_merge)
ggplot(total_pr_merge, aes(recall,precision, color=Type)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "P-R curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) 
ggsave('rice/pr_TSARC_TSSPlant_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)




#   cotton 


setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/TSARP_versus_other_software/')
# TSARP
TSARP_roc <- read.csv('cotton/ROC_Curve_fold10_data.csv')
TSARP_roc$Type <- 'TSARC'

# TransPrise
tr_roc <- read.csv('cotton/ROC_Curve_data_TransPrise.csv')
tr_roc$Type <- 'TransPrise'

# TSSPlant
tp_roc <- read.csv('cotton/ROC_Curve_data_TSSPlant.csv')
tp_roc$Type <- 'TSSPlant'

# one figure 
total_roc_merge <- rbind(TSARP_roc, tp_roc, tr_roc)
head(total_roc_merge)
ggplot(total_roc_merge, aes(fpr,tpr, color=Type)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0))
ggsave('cotton/roc_TSARC_TSSPlant_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)

# PR 
TSARP_pr <- read.csv('cotton/PR_Curve_mean_data.csv')
TSARP_pr$Type <- 'TSARC'
head(TSARP_pr)

tr_pr <- read.csv('cotton/PR_Curve_data_TransPrise.csv')
tr_pr$Type <- 'TransPrise'
head(tr_pr)

tp_pr <- read.csv('cotton/PR_Curve_data_TSSPlant.csv')
tp_pr$Type <- 'TSSPlant'
head(tp_pr)

# one figure 
total_pr_merge <- rbind(TSARP_pr, tp_pr, tr_pr)
head(total_pr_merge)
ggplot(total_pr_merge, aes(recall,precision, color=Type)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "P-R curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) 
ggsave('cotton/pr_TSARC_TSSPlant_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)


#     maize 

setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/TSARP_versus_other_software/')
# TSARP
TSARP_roc <- read.csv('maize/ROC_Curve_fold10_data.csv')
TSARP_roc$Type <- 'TSARC'

# TransPrise
tr_roc <- read.csv('maize/ROC_Curve_data_TransPrise.csv')
tr_roc$Type <- 'TransPrise'

# TSSPlant
tp_roc <- read.csv('maize/ROC_Curve_data_TSSPlant.csv')
tp_roc$Type <- 'TSSPlant'

# one figure 
total_roc_merge <- rbind(TSARP_roc, tp_roc, tr_roc)
head(total_roc_merge)
ggplot(total_roc_merge, aes(fpr,tpr, color=Type)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0))
ggsave('maize/roc_TSARC_TSSPlant_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)

# PR 
TSARP_pr <- read.csv('maize/PR_Curve_fold10_data.csv')
TSARP_pr$Type <- 'TSARC'
head(TSARP_pr)

tr_pr <- read.csv('maize/PR_Curve_data_TransPrise.csv')
tr_pr$Type <- 'TransPrise'
head(tr_pr)

tp_pr <- read.csv('maize/PR_Curve_data_TSSPlant.csv')
tp_pr$Type <- 'TSSPlant'
head(tp_pr)

# one figure 
total_pr_merge <- rbind(TSARP_pr, tp_pr, tr_pr)
head(total_pr_merge)
ggplot(total_pr_merge, aes(recall,precision, color=Type)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "P-R curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) 
ggsave('maize/pr_TSARC_TSSPlant_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)

#    soybean 
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/TSARP_versus_other_software/')
# TSARP
TSARP_roc <- read.csv('soybean/ROC_Curve_fold10_data.csv')
TSARP_roc$Type <- 'TSARC'

# TransPrise
tr_roc <- read.csv('soybean/ROC_Curve_data_TransPrise.csv')
tr_roc$Type <- 'TransPrise'

# TSSPlant
tp_roc <- read.csv('soybean/ROC_Curve_data_TSSPlant.csv')
tp_roc$Type <- 'TSSPlant'

# one figure 
total_roc_merge <- rbind(TSARP_roc, tp_roc, tr_roc)
head(total_roc_merge)
ggplot(total_roc_merge, aes(fpr,tpr, color=Type)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0))
ggsave('soybean/roc_TSARC_TSSPlant_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)

# PR 
TSARP_pr <- read.csv('soybean/PR_Curve_fold10_data.csv')
TSARP_pr$Type <- 'TSARC'
head(TSARP_pr)

tr_pr <- read.csv('soybean/PR_Curve_data_TransPrise.csv')
tr_pr$Type <- 'TransPrise'
head(tr_pr)

tp_pr <- read.csv('soybean/PR_Curve_data_TSSPlant.csv')
tp_pr$Type <- 'TSSPlant'
head(tp_pr)

# one figure 
total_pr_merge <- rbind(TSARP_pr, tp_pr, tr_pr)
head(total_pr_merge)
ggplot(total_pr_merge, aes(recall,precision, color=Type)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "P-R curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) 
ggsave('soybean/pr_TSARC_TSSPlant_TransPrise.pdf',width = 8, height = 6,units = 'in',dpi=300)
