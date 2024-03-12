# 画sun test方法和我们自己的额frequency的方法看两者找到的代表性转录本的差异
library(ggplot2)
library(ggVennDiagram)
#install.packages('ggbreak')
library(ggbreak)
library(ggsci)
# 第一次计算
# /home/zhusitao/database/plant/ath/RNA/Dzjx/test/accumulate.py
# /home/zhusitao/database/plant/ath/RNA/Dzjx/test/principal_freq_cumulative.csv
# 第二次计算
# accumulate.py
# /home/zhusitao/database/plant/ath/RNA/Dzjx/Principal_Freq/principal_freq_cumulative.csv
# 第三次计算
# /data/zhusitao/database/plant/ath/RNA/13.RSEM_ALL/Rank_Value_Order/Principal_Freq/principal_freq_cumulative.csv
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/Benchmark/')

# 第四次计算
# 被检测该基因的样本数作为分母
# /data/zhusitao/database/plant/ath/RNA/13.RSEM_ALL/Rank_Value_Order/Principal_Freq/total_table
#cumulative
# 第5次计算，使用的是rank, 在这些样本中他作为principal isoform
# RSEM eXpress FLAIR
# /data/zhusitao/database/plant/ath/RNA/15.eXpress/Principal_Freq/total_table/rank_algorithm_comparation.py
df <- read.csv('principal_freq_cumulative_comparation.csv')
dim(df)
# df <- read.csv('/Users/zhusitao/Downloads/principal_freq_cumulative.csv')
df
ggplot(data = df, aes(x=Ratio_cumulative, y=Principal_ratio, color=software)) +
  geom_line() + theme_classic() +
  scale_x_continuous(breaks = c(0,0.2,0.4,0.6,0.8,1)) +
  scale_y_continuous(breaks = c(0,0.2,0.4,0.6,0.8,1), limits = c(0,1)) +
  geom_hline(yintercept=0.30) 
  #scale_x_break(c(0.9,0.99),scales = c(0.1,0.001))

ggplot(data = df, aes(x=Ratio_cumulative, y=Principal_ratio, color=software)) +
  geom_line() + theme_classic() +
  scale_y_continuous(breaks = c(0,0.2,0.4,0.6,0.8,1), limits = c(0,1)) +
  geom_vline(xintercept=0.9) + scale_color_npg()
ggsave('principal_isoform_frequency_0_1.pdf',width = 8, height = 6,units = 'in',dpi=300)

ggplot(data = df, aes(x=Ratio_cumulative, y=Principal_ratio, color=software)) +
  geom_line() + theme_classic() +
  xlim(0.8,1) +
  scale_y_continuous(breaks = c(0,0.2,0.4,0.6,0.8,1), limits = c(0,1)) +
  geom_vline(xintercept=0.9) + scale_color_npg()
ggsave('principal_isoform_frequency.pdf',width = 8, height = 6,units = 'in',dpi=300)




# manual check
library(ggpubr)
df <- read.csv('browser_check_ratio.csv')
head(df)

head(df)
ggplot(data = df, aes(x=Source, y=Accuracy, )) + geom_boxplot() + 
  geom_point(position = position_jitter(width = 0.1), aes(color=Source)) +
  theme_classic() + stat_compare_means(method = 't.test')
  
ggsave('representative_comparison_in_browser.pdf',width = 8, height = 6,units = 'in',dpi=300)
