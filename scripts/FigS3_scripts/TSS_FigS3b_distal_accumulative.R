library(ggplot2)
library(ggVennDiagram)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/distal_logical/')
# /home/zhusitao/project/DPI/01.ath/tissue/v2_get_distal_logical.py
# 新版本 /home/zhusitao/project/DPI/01.ath/tissue_new


#cumulative 方法1 使用 tissue DPI permissive 
df <- read.csv('distal_freq_ratio.csv')
dim(df)
head(df)
ggplot(data = df, aes(x=Ratio_cumulative, y=Robust_ratio)) +
  geom_line() + theme_classic() +
  scale_x_continuous(breaks = c(0,0.2,0.4,0.6,0.8,1)) +
  scale_y_continuous(breaks = c(0,0.2,0.4,0.6,0.8,1), limits = c(0,1)) +
  geom_vline(xintercept=0.5)
ggsave('distal_representative_tissue.pdf',width = 8, height = 6,units = 'in',dpi=300)

# 方法2 使用样本频数和tag
# df <- read.csv('distal_tag_ratio.csv')
df <- read.csv('distal_tag_ratio_0421.csv')
dim(df)
head(df)
ggplot(data = df, aes(x=Ratio_cumulative, y=Robust_ratio)) +
  geom_line() + theme_classic() +
  scale_x_continuous(breaks = c(0,0.2,0.4,0.6,0.8,1)) +
  scale_y_continuous(breaks = c(0,0.2,0.4,0.6,0.8,1), limits = c(0,1)) +
  geom_vline(xintercept=0.5)

# ggsave('distal_representative_tag.pdf',width = 8, height = 6,units = 'in',dpi=300)
ggsave('distal_representative_tag_0421.pdf',width = 8, height = 6,units = 'in',dpi=300)


# 论证distal具有代表性
# 画出distal 倒数第二个，倒数第三个的
distal_df <- read.csv('distal_tag_ratio_0421.csv')
distal_df$Type <- 'Distal_peak'
head(distal_df)

second_df <- read.csv('Second_distal_tag_ratio.csv')
second_df$Type <- 'Second_peak'
head(second_df)

third_df <- read.csv('Third_distal_tag_ratio.csv')
third_df$Type <- 'Third_peak'
head(third_df)

total_df <- rbind(distal_df, second_df, third_df)
head(total_df)
ggplot(data = total_df, aes(x=Ratio_cumulative, y=Robust_ratio, color=Type)) +
  geom_line() + theme_classic() +
  scale_x_continuous(breaks = c(0,0.2,0.4,0.6,0.8,1)) +
  scale_y_continuous(breaks = c(0,0.2,0.4,0.6,0.8,1), limits = c(0,1)) +
  geom_vline(xintercept=0.5) + ylab('Accumulative frequency') + xlab('Sample ratio')
ggsave('distal_representative_tag_second_third.pdf',width = 8, height = 6,units = 'in',dpi=300)


# p1 p2 p3 density in five species 
# /home/zhusitao/project/DPI/01.ath/tissue_new/get_p123_frequency_total.py
# /home/zhusitao/project/DPI/01.ath/tissue_new/Total_furthest_second_third.csv
df <- read.csv('Total_furthest_second_third.csv')
head(df)
library(ggsci)
library(ggpubr)
my_comparisons <- list( c("Furthest", "Second"), c("Furthest", "Third"), c("Second", "Third"))
ggplot(data = df, aes(x = Type, y = Ratio)) + 
  geom_boxplot( width = 0.7) +
  theme_classic() + scale_fill_npg() + 
  stat_compare_means(comparisons = my_comparisons, method = "t.test", ref.group = "utr5") +
  geom_line(aes(group = Species, color=Species), linetype=2) +
  scale_color_npg() 
df$LogRatio <- log2(df$Ratio)
head(df)
ggplot(data = df, aes(x = Type, y = LogRatio)) + 
  geom_boxplot( width = 0.7) +
  theme_classic() + scale_fill_npg() + 
  stat_compare_means(comparisons = my_comparisons, method = "t.test", ref.group = "utr5") +
  geom_line(aes(group = Species, color=Species), linetype=2) +
  scale_color_npg() 
ggsave('furthest_second_third_ratio.pdf',width = 8, height = 6,units = 'in',dpi=300)

