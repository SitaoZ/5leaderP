library(ggplot2)
library(reshape2)
# ath 
# robust 
# program: get_peak.py get_95X.py
# path: /home/zhusitao/project/DPI/01.ath/CTSS_for_DPI/robust_permissive_curve/robust_peak_region.csv
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/peak_norm/')
df <- read.csv('robust_peak_region.csv')
ggplot(df, aes(x=X, y=Y)) + geom_bar(stat = 'identity', fill='#2F9830') +
  xlim(-75,75) +
  geom_vline(xintercept =-31, linetype="dotted", color = "blue", size=1) +
  geom_vline(xintercept =32, linetype="dotted", color = "blue", size=1) +
  theme_classic() +
  annotate("text", x = -31, y = 1000, label = "x = -31") +
  annotate("text", x = 32, y = 1000, label = "x = 32")
ggsave('ath_robust_peak_region.pdf',width = 8, height = 6,units = 'in',dpi=300)
# permissive
# /home/zhusitao/project/DPI/01.ath/CTSS_for_DPI/robust_permissive_curve/permissive_peak_region.csv
df <- read.csv('permissive_peak_region.csv')
ggplot(df, aes(x=X, y=Y)) + geom_bar(stat = 'identity', fill='#B2D988') +
  xlim(-75,75) +
  geom_vline(xintercept =-25, linetype="dotted", color = "blue", size=1) +
  geom_vline(xintercept =25, linetype="dotted", color = "blue", size=1) +
  theme_classic() +
  annotate("text", x = -25, y = 2000, label = "x = -25") +
  annotate("text", x = 25, y = 2000, label = "x = 25")
ggsave('ath_permissive_peak_region.pdf',width = 8, height = 6,units = 'in',dpi=300)


# osa 
# /home/zhusitao/project/DPI/02.rice/NIP_for_DPI/robust_permissive_curve
df <- read.csv('osa_permissive_peak_region.csv')
ggplot(df, aes(x=X, y=Y)) + geom_bar(stat = 'identity') +
  xlim(-75,75) +
  geom_vline(xintercept =-29, linetype="dotted", color = "blue", size=1) +
  geom_vline(xintercept =30, linetype="dotted", color = "blue", size=1) +
  theme_classic() +
  annotate("text", x = -29, y = 2000, label = "x = -29") +
  annotate("text", x = 30, y = 2000, label = "x = 30")
ggsave('osa_permissive_peak_region.pdf',width = 8, height = 6,units = 'in',dpi=300)

# cotton
# /home/zhusitao/project/DPI/03.cotton/CTSS_for_DPI/robust_permissive_curve
df <- read.csv('gab_robust_peak_region.csv')
ggplot(df, aes(x=X, y=Y)) + geom_bar(stat = 'identity') +
  xlim(-75,75) +
  geom_vline(xintercept =-21, linetype="dotted", color = "blue", size=1) +
  geom_vline(xintercept =19, linetype="dotted", color = "blue", size=1) +
  theme_classic() +
  annotate("text", x = -21, y = 2000, label = "x = -21") +
  annotate("text", x = 19, y = 2000, label = "x = 19")
ggsave('gab_robust_peak_region.pdf',width = 8, height = 6,units = 'in',dpi=300)

df <- read.csv('gab_permissive_peak_region.csv')
ggplot(df, aes(x=X, y=Y)) + geom_bar(stat = 'identity') +
  xlim(-75,75) +
  geom_vline(xintercept =-22, linetype="dotted", color = "blue", size=1) +
  geom_vline(xintercept =20, linetype="dotted", color = "blue", size=1) +
  theme_classic() +
  annotate("text", x = -22, y = 2000, label = "x = -22") +
  annotate("text", x = 20, y = 2000, label = "x = 20")
ggsave('gab_permissive_peak_region.pdf',width = 8, height = 6,units = 'in',dpi=300)


# maize
# /home/zhusitao/project/DPI/04.maize/CTSS_for_DPI/robust_permissive_curve
df <- read.csv('zma_robust_peak_region.csv')
ggplot(df, aes(x=X, y=Y)) + geom_bar(stat = 'identity') +
  xlim(-75,75) +
  geom_vline(xintercept =-19, linetype="dotted", color = "blue", size=1) +
  geom_vline(xintercept =18, linetype="dotted", color = "blue", size=1) +
  theme_classic() +
  annotate("text", x = -19, y = 2000, label = "x = -19") +
  annotate("text", x = 18, y = 2000, label = "x = 18")
ggsave('zma_robust_peak_region.pdf',width = 8, height = 6,units = 'in',dpi=300)

df <- read.csv('zma_permissive_peak_region.csv')
ggplot(df, aes(x=X, y=Y)) + geom_bar(stat = 'identity') +
  xlim(-75,75) +
  geom_vline(xintercept =-21, linetype="dotted", color = "blue", size=1) +
  geom_vline(xintercept =20, linetype="dotted", color = "blue", size=1) +
  theme_classic() +
  annotate("text", x = -21, y = 2000, label = "x = -21") +
  annotate("text", x = 20, y = 2000, label = "x = 20")
ggsave('zma_permissive_peak_region.pdf',width = 8, height = 6,units = 'in',dpi=300)

# soybean
# /home/zhusitao/project/DPI/05.soybean/CTSS_for_DPI/robust_permissive_curve 
df <- read.csv('gmx_permissive_peak_region.csv')
ggplot(df, aes(x=X, y=Y)) + geom_bar(stat = 'identity') +
  xlim(-75,75) +
  geom_vline(xintercept =-29, linetype="dotted", color = "blue", size=1) +
  geom_vline(xintercept =31, linetype="dotted", color = "blue", size=1) +
  theme_classic() +
  annotate("text", x = -29, y = 2000, label = "x = -29") +
  annotate("text", x = 31, y = 2000, label = "x = 31")
ggsave('gmx_permissive_peak_region.pdf',width = 8, height = 6,units = 'in',dpi=300)



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


## for 毕业论文 5个物种和总的分布
# /home/zhusitao/project/DPI/05.soybean/CTSS_for_DPI/robust_permissive_curve/total/dissertation/tags_permissive.csv

library(ggsci)
plant <- read.csv('tags_permissive.csv')
head(plant)
X95 <- read.csv('X95_line.csv')
X95
ggplot(data = plant, aes(x = X, y = SUM, fill = Species)) + 
  geom_bar(stat = 'identity') +
  xlim(-75,75) + theme_classic() +
  geom_vline(data = X95, aes(xintercept = X1, color = Species)) +
  geom_vline(data = X95, aes(xintercept = X2, color = Species)) +
  facet_wrap(~Species) + scale_fill_npg() + scale_color_npg()
ggsave('total_permissive_x95.pdf',width = 8, height = 6,units = 'in',dpi=300)
