# regression model performance 

# version 20230220
# /home/zhusitao/AI/TSS_Predict/ath/final_version/class/github/current/ResNet/test/roc_pr_species.csv
# /home/zhusitao/AI/TSS_Predict/ath/final_version/class/github/current/ResNet/test/get_total_cross.py

# version 20230322
# version 20230421
library(ggplot2)
library(reshape2)

# FigS6b
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/cross_species/')
df <- read.csv('20230421/roc_pr_species.csv')
head(df)
melt_df <- melt(df, id= c('species', 'stype'))
head(melt_df)
ggplot(data = melt_df, aes(x = variable, y = value, fill=stype)) +
  geom_boxplot(outlier.shape = NA) +
  theme_classic() + 
  ylab('AUC') 
ggsave('20230421/cross_species_roc_pr.pdf',width = 8, height = 6,units = 'in',dpi=300)

# FigS6b for 毕业论文
ggplot(data = melt_df, aes(x = variable, y = value, color=stype)) +
  geom_boxplot(outlier.shape = NA) +
  theme_classic() + 
  ylab('AUC') + 
  geom_point(aes(colour = stype),
             position = position_jitterdodge(jitter.width = 0.2)) 


ggsave('20230421/cross_species_roc_pr_ponit.pdf',width = 8, height = 6,units = 'in',dpi=300)


# FigS7b 
# R2 in regression model 
# /home/zhusitao/AI/TSS_Predict/species_r2
# r2 <- read.csv("20230220/species_r2.csv")
# r2 <- read.csv("20230322/species_r2.csv")
r2 <- read.csv("20230421/species_r2.csv")
head(r2)
ggplot(data = r2, aes(x = Type, y = R2, color = Type)) +
  geom_boxplot() + theme_classic()
ggsave('20230421/cross_species_r2.pdf',width = 8, height = 6,units = 'in',dpi=300)

# add point for 毕业论文
r2$Type <- factor(r2$Type, levels = c("species_specific_self", "species_specific_other", "general"))
ggplot(data = r2, aes(x = Type, y = R2, color = Type)) +
  geom_boxplot() + theme_classic() +geom_jitter(width = 0.1)
ggsave('20230421/cross_species_r2_point.pdf',width = 8, height = 6,units = 'in',dpi=300)
