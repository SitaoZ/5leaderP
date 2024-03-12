# general model performance 
library(ggplot2)
library(RColorBrewer)
?RColorBrewer
display.brewer.all(n=NULL, type="all", select=NULL, exact.n=TRUE, 
                   colorblindFriendly=FALSE)
mypalette <- brewer.pal(7,"Set1")

simple_auc <- function(TPR, FPR){
  # inputs already sorted, best scores first 
  dFPR <- c(diff(FPR), 0)
  dTPR <- c(diff(TPR), 0)
  sum(TPR * dFPR) + sum(dTPR * dFPR)/2
}
# path on linux cluster
# /home/zhusitao/AI/TSS_Predict/PlantModel/final_version/class/github/current/ResNet/setaria
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/general_model_performance/')
setaria <- read.csv('Setaria_viridis/roc_merge_average.csv')
setaria['Type'] <- 'Setaria viridis'
simple_auc(setaria$tpr, setaria$fpr)

TX2783 <- read.csv('Sorghum_bicolor/TX2783//roc_merge_average.csv')
TX2783['Type'] <- 'TX2783 (Sorghum bicolor)'
simple_auc(TX2783$tpr, TX2783$fpr)

tx436 <- read.csv('Sorghum_bicolor/tx436/roc_merge_average.csv')
tx436['Type'] <- 'tx436 (Sorghum bicolor)'
simple_auc(tx436$tpr, tx436$fpr)

roc <- rbind(setaria, tx436, TX2783)
ggplot(roc, aes(fpr,tpr, color = Type)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "ROC curve", 
       x = "False Positive Rate (1-Specificity)", 
       y = "True Positive Rate (Sensitivity)") +
  theme_classic() +
  geom_abline(linetype = 'dashed') +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  annotate("text", x = 0.8, y=c(0.1, 0.14, 0.18), 
           label = c('AUC = 0.9587832', 'AUC = 0.9793849', 'AUC = 0.9802294')) +
  scale_colour_manual(values=mypalette)

ggsave('general_test_roc_curve.pdf',width = 8, height = 6,units = 'in',dpi=300)

# PR
setaria <- read.csv('Setaria_viridis/pr_merge_average.csv')
setaria['Type'] <- 'Setaria viridis'

TX2783 <- read.csv('Sorghum_bicolor/TX2783/pr_merge_average.csv')
TX2783['Type'] <- 'TX2783 (Sorghum bicolor)'


tx436 <- read.csv('Sorghum_bicolor/tx436/pr_merge_average.csv')
tx436['Type'] <- 'tx436 (Sorghum bicolor)'

pr <- rbind(setaria, tx436, TX2783)

ggplot(pr,aes(recall,precision, color=Type)) + 
  geom_line(size = 1, alpha = 1) +
  labs(title= "PR curve", 
       x = "Recall", 
       y = "Precision") +
  theme_classic() +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  scale_colour_manual(values=mypalette)

ggsave('general_test_pr_curve.pdf',width = 8, height = 6,units = 'in',dpi=300)
