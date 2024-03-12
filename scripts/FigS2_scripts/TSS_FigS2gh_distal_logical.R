# TSS distal peak logical 

library(ggplot2)

# /home/zhusitao/project/DPI/01.ath/tissue/get_distal_logical.py
# /home/zhusitao/project/DPI/01.ath/tissue/v2_get_distal_logical.py
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/distal_logical/')

ath <- read.csv('ath/MAE.csv', header = FALSE)
head(ath)
colnames(ath) <- c('MAE', 'Species')
head(ath)

gab <- read.csv('gab/MAE.csv', header = FALSE)
colnames(gab) <- c('MAE', 'Species')

zma <- read.csv('zma/MAE.csv', header = FALSE)
colnames(zma) <- c('MAE', 'Species')

gmx <- read.csv('gmx/MAE.csv', header = FALSE)
colnames(gmx) <- c('MAE', 'Species')

df <- rbind(ath, gab, zma, gmx)

ggplot(data = df, aes(x = Species, y = MAE, color=Species)) + 
  geom_boxplot(outlier.shape = NA, width=0.8) +
  ylim(0,3) +
  theme_classic()
ggsave('distal_logical_mae.pdf',width = 8, height = 6,units = 'in',dpi=300)


pp <- read.csv('portion.csv')
head(pp)
ggplot(data = pp, aes(x = Tissue, y = Portion, fill=Source)) + 
  geom_bar(stat = 'identity',position = 'dodge') + theme_classic() +
  scale_fill_brewer(palette = 'Set2') + xlab('Number of tissues ') +
  ylab('Portion of distal peak covered in tissues')
ggsave('distal_logical_portion.pdf',width = 8, height = 6,units = 'in',dpi=300)
