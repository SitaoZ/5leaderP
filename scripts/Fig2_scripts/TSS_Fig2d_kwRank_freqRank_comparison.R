# 画sun test方法和我们自己的额frequency的方法看两者找到的代表性转录本的差异
library(ggplot2)
library(ggVennDiagram)
#install.packages('ggbreak')
library(ggbreak)
library(ggsci)

# RSEM eXpress FLAIR
# /data/zhusitao/database/plant/ath/RNA/15.eXpress/Principal_Freq/total_table/rank_algorithm_comparation.py
df <- read.csv('principal_freq_cumulative_comparation.csv')
dim(df)

ggplot(data = df, aes(x=Ratio_cumulative, y=Principal_ratio, color=software)) +
  geom_line() + theme_classic() +
  scale_y_continuous(breaks = c(0,0.2,0.4,0.6,0.8,1), limits = c(0,1)) +
  geom_vline(xintercept=0.9) + scale_color_npg()
ggsave('principal_isoform_frequency_0_1.pdf',width = 8, height = 6,units = 'in',dpi=300)
