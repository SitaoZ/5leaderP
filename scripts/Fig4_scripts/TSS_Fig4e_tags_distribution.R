library(ggplot2)
library(reshape2)
# ath 
# robust 
# program: get_peak.py get_95X.py
# path: /home/zhusitao/project/DPI/01.ath/CTSS_for_DPI/robust_permissive_curve/robust_peak_region.csv


# total
# /home/zhusitao/project/DPI/05.soybean/CTSS_for_DPI/robust_permissive_curve/total/get_total_permissive.py
# 合并ath,gab,zma得到total_robust.csv
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/peak_norm/')
total <- read.csv('total_robust.csv')
head(total)
dim(total)
ggplot(total, aes(x=X, y=SUM)) + geom_bar(stat = 'identity', fill='#2F9830') +
  xlim(-75,75) +
  geom_vline(xintercept =-24, linetype="dotted", color = "blue", size=1) +
  geom_vline(xintercept =23, linetype="dotted", color = "blue", size=1) +
  theme_classic() +
  annotate("text", x = -24, y = 2000, label = "x = -24") +
  annotate("text", x = 23, y = 2000, label = "x = 23")
ggsave('total_robust_peak_region.pdf',width = 8, height = 6,units = 'in',dpi=300)


# 合并ath,osa,gab,zma,gmx得到total_permissive.csv
total <- read.csv('total_permissive.csv')
head(total)
dim(total)
ggplot(total, aes(x=X, y=SUM)) + geom_bar(stat = 'identity', fill='#B2D988') +
  xlim(-75,75) +
  geom_vline(xintercept =-25, linetype="dotted", color = "blue", size=1) +
  geom_vline(xintercept =26, linetype="dotted", color = "blue", size=1) +
  theme_classic() +
  annotate("text", x = -25, y = 2000, label = "x = -25") +
  annotate("text", x = 26, y = 2000, label = "x = 26")
ggsave('total_permissive_peak_region.pdf',width = 8, height = 6,units = 'in',dpi=300)

# 画成一个图， robust permissive
robust <- read.csv('total_robust.csv')
robust_filter <- robust[c("X", "SUM")]
robust_filter$Type <- 'robust'
head(robust_filter)
permissive <- read.csv('total_permissive.csv')
permissive_filter <- permissive[c("X","SUM")]
permissive_filter$Type <- 'permissive'
head(permissive_filter)
robust_permissive <- rbind(robust_filter, permissive_filter)
ggplot(robust_permissive, aes(x=X, y=SUM, fill=Type)) + geom_bar(stat = 'identity') +
  xlim(-75,75) +
  geom_vline(xintercept =-25, linetype="dotted", color = "blue", size=1) +
  geom_vline(xintercept =26, linetype="dotted", color = "blue", size=1) +
  theme_classic() +
  annotate("text", x = -25, y = 2000, label = "x = -25") +
  annotate("text", x = 26, y = 2000, label = "x = 26") + scale_fill_brewer(palette = 'Set2')
ggsave('total_robust_permissive_peak_region.pdf',width = 8, height = 6,units = 'in',dpi=300)
