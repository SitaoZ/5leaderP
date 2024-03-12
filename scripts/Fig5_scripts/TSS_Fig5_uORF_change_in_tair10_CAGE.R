# Figure 5

library(ggplot2)
library(gg.gap)
library(ggpubr)
library(ggpmisc)
library(RColorBrewer)
display.brewer.all( type = 'all')
mypalette <- brewer.pal(n = 8, 'Paired')

# TBF1 prediction (a. 采用示意图形式)

# Fig5f
# 新添加fig5a exp/pred的占比每个物种中
# /home/zhusitao/database/plant/ath/merge_gff/01.merge/current/mani/gff_inherit/All_Archetypal_isoforms_Arabidopsis_V1.0/GeneID/exp_pred_ratio/get_exp_pred.py
# total_exp_pred.csv
library(ggsci)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/uORF_tair10_CAGE/')
total_ratio = read.csv('total_exp_pred.csv')
head(total_ratio)
ggplot(data = total_ratio, aes(x = Species, y = Ratio, fill = PeakSource)) +
  geom_bar(stat = 'identity',position = "stack", width = 0.7) + scale_fill_npg() + theme_classic()
ggsave('exp_pred_species.pdf',width = 8, height = 6,units = 'in',dpi=300)


# Fig 5d
# 其他四个物种的uORF变化情况，附图
# /home/zhusitao/project/DPI/10.uORF_change/get_data.py
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/uORF_tair10_CAGE/')
ad <- read.csv('uORF_ad_type/Archetypal/uORF_ad.csv')

head(ad)
ggplot(data = ad, aes(x = Species, y = Count, fill=Source)) +
  geom_bar(stat = 'identity', position = 'dodge', width = 0.7) +
  theme_classic() + scale_fill_manual(values=c('longest'='#EF7F1B', 'truncated'='#1F78AC'))
# scale_fill_manual(values=mypalette[3:4]) 
ggsave('uORF_ad_type/Archetypal/uORF_add_delete.pdf',width = 8, height = 6,units = 'in',dpi=300)


#Fig 5e
utype <- read.csv('uORF_ad_type/Archetypal/uORF_utype.csv')
head(utype)
dim(utype)
# remove Type3
library(dplyr)
utype <- filter(utype, Type!='type3')
dim(utype)
# 分页
#ggplot(data = utype, aes(x = Type, y = Count, fill=Source)) +
#  geom_bar(stat = 'identity', position = 'dodge', width = 0.5) +
#  theme_classic() + scale_fill_manual(values=mypalette) +
#  facet_wrap(~Species, scales = 'free')
#  facet_grid(rows = vars(Species), scales = 'free')
  
# 堆叠
library(ggplot2)
library(ggpattern)
# remotes::install_github("coolbutuseless/ggpattern")
ggplot(data = utype, aes(x = Species, y = Count, fill=Type)) +
  geom_bar(aes(group=Source, color=Source),stat = 'identity', position = 'dodge', width = 0.5) +
  theme_classic() + scale_fill_manual(values=brewer.pal(n = 8, 'Set2')) +
  scale_color_manual(values=brewer.pal(n = 8, 'Set1')) 

# pattern 
p1 = ggplot(utype, aes(x = Species, y = Count, fill = Type)) +
  geom_col_pattern(
    aes(pattern = Source, group=Source),
    colour = "black",
    pattern_fill = "black",
    pattern_angle = 45,
    pattern_density = 0.1,
    pattern_spacing = 0.01,
    width = 0.7,
    position = position_dodge(preserve = 'total'),
  ) +
  scale_pattern_manual(
    values = c("none", "stripe"),
    guide = guide_legend(override.aes = list(fill = "grey70")) # <- make lighter
  ) +
  scale_fill_discrete(
    guide = guide_legend(override.aes = list(pattern = "none")) # <- hide pattern
  ) +
  theme_classic() 
pdf("uORF_ad_type/Archetypal/uORF_type12.pdf",width=8,height=6)
p1
dev.off()
