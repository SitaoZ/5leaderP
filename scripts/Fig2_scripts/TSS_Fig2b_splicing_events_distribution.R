# splicing on region 
library(ggplot2)
library(RColorBrewer)
library(dplyr)
library(ggpubr)
library(ggsci)


setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/Benchmark/')
# 不再使用 /home/zhusitao/database/plant/ath/merge_gff/04.decoder/transdecoder/fig2c_as/fig2c_data.csv
# 使用最新版本
# /home/zhusitao/database/plant/ath/merge_gff/01.merge/current/mani/gff_inherit/All_Archetypal_isoforms_Arabidopsis_V1.0/fig2c_as/fig2c_data.csv
# df <- read.csv('fig2c_data.csv')
# 相比之前的版本在 CDS/UTR5 共变化中除去了aTSS的变化；在UTR5/UTR3的共变化中除去aTSS的变化；
df <- read.csv('fig2c_data_20230412.csv')
head(df)

df <- filter(df, Source=="AS")
df

df$Region <- factor(df$Region, levels = c('utr5', 'utr5_cds', 'utr5_utr3'))
ggplot(data = df, aes(x = Region, y = Ratio, fill=Source)) + 
  geom_bar(stat = 'identity', position = 'dodge') +
  theme_classic() + scale_fill_brewer(palette = 'Paired') +
  geom_text(aes(label=round(Ratio, 4)), vjust = 1, position = position_dodge(width = 0.9))

ggplot(data = df, aes(x = Region, y = Ratio, fill=Region)) + 
  geom_bar(stat = 'identity', width = 0.7) +
  theme_classic() + scale_fill_brewer(palette = 'Set2') +
  geom_text(aes(label=round(Ratio, 4)), vjust = 1, position = position_dodge(width = 0.9))


ggsave('splicing_distribution.pdf',width = 8, height = 6,units = 'in',dpi=300)

# 其他四个物种也计算了
# rice cotton maize soybean ,趋势相同
# /home/zhusitao/database/plant/*/merge_gff/01.merge/mani/gff_inherit/All_Archetypal_isoforms_Arabidopsis_V1.0/fig2c_as/fig2c_data_20230412.csv



# 画成一个图
# /home/zhusitao/database/plant/ath/merge_gff/01.merge/current/mani/gff_inherit/All_Archetypal_isoforms_Arabidopsis_V1.0/GeneID/fig2c_as/get_total_fig2c_as.py
df <- read.csv('total_fig2c_20230531.csv')
head(df)
df$LogRation <- log2(df$Ratio)
head(df)
# Pairwise comparisons: Specify the comparisons you want
my_comparisons <- list( c("utr5", "utr5_cds"), c("utr5", "utr5_utr3"), c("utr5_cds", "utr5_utr3") )
ggplot(data = df, aes(x = Region, y = LogRation, fill=Region)) + 
  geom_boxplot( width = 0.7) +
  theme_classic() + scale_fill_brewer(palette = 'Set2') + 
  stat_compare_means(aes(label = ..p.signif..),
                     method = "t.test", ref.group = "utr5") +
  geom_line(aes(group = Species, color=Species))

ggsave('splicing_distribution_remove_aTSS_PAS.pdf',width = 8, height = 6,units = 'in',dpi=300)



ggplot(data = df, aes(x = Region, y = LogRation)) + 
  geom_boxplot( width = 0.7) +
  theme_classic() + scale_fill_npg() + 
  stat_compare_means(comparisons = my_comparisons, method = "t.test", ref.group = "utr5") +
  geom_line(aes(group = Species, color=Species), linetype=2) +
  scale_color_npg() 

ggsave('splicing_distribution_remove_aTSS_PAS_add_line.pdf',width = 8, height = 6,units = 'in',dpi=300)

