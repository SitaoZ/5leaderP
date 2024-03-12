# figure 5

library(ggplot2)
library(gg.gap)
library(ggpubr)
library(ggpmisc)
library(RColorBrewer)
display.brewer.all( type = 'all')
mypalette <- brewer.pal(n = 8, 'Paired')

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
# TBF1 prediction (a. 采用示意图形式)
# /home/zhusitao/AI/TSS_Predict/ath/final_version/regress/peakCount_tanh
#df <- read.csv('TBF1_ggplot2.csv')
#my.formula <- x ~ y
##ggplot(data = df, aes(x = tbf_pred, y = tbf_true)) +
#  geom_point(alpha=0.6,color='black', size=0.8) + theme_classic()

#mae <- data.frame('Count'=c(14.21), 'Type'=c('MAE'))
#mae
#ggplot(data = mae, aes(x = Type, y = Count)) + geom_bar(stat = 'identity')

setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/uORF_tair10_CAGE/')

# uORF Type
# /home/zhusitao/project/DPI/01.ath/peak_process/11.represent_gff/uORF_compare/CAGE
df <- read.csv('uORF_type.csv')
df
p1 = ggplot(data = df, aes(x = Type, y = Count, fill=Source)) + 
  geom_bar(stat = 'identity', position = 'dodge') + 
  theme_classic() + scale_fill_manual(values=mypalette[3:4])

ggsave('uORF_type_legend.pdf',width = 8, height = 6,units = 'in',dpi=300)
p1
gg.gap(plot = p1,
           segments = c(200, 1000),
           tick_width = c(100, 10000),
           rel_heights = c(0.25, 0, 0.1),
           ylim = c(0, 35000)
)
ggsave('uORF_type.pdf',width = 8, height = 6,units = 'in',dpi=300)


# uORF add and delete
# /home/zhusitao/project/DPI/01.ath/peak_process/11.represent_gff/uORF_compare/CAGE
df <- read.csv('uORF_add_delete.csv')
df
ggplot(data = df, aes(x = Change, y = Count, fill=Change)) + 
  geom_bar(stat = 'identity', position = 'dodge', width = 0.5) + 
  theme_classic() + scale_fill_manual(values=mypalette[7:8])
ggsave('uORF_change.pdf',width = 8, height = 6,units = 'in',dpi=300)

# abcd
# /home/zhusitao/AI/TSS_Predict/ath/final_version/regress/peakCount_tanh
# setwd('/Users/zhusitao/Downloads/')
df <- read.csv('abcd.csv')
head(df)
df
mean(df$Count)
ggplot(data = df, aes(x = Source, y = Count, fill=Source)) +
  geom_boxplot() + theme_classic() + scale_fill_manual(values=mypalette)
ggsave('abcd.pdf',width = 8, height = 6,units = 'in',dpi=300)

#### 最终图，上面的都是测试的脚本 ####--------------------------------------------------
# Fig 5b
# prominent longest
# /home/zhusitao/project/DPI/11.prominent_longest/work.sh
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/uORF_tair10_CAGE/')
df <- read.csv('prominent_longest/all_prominent_longest.csv', header = FALSE)
head(df)
colnames(df) <- c('Distance', 'Species','Source')
head(df)
ggplot(data = df, aes(x = Species, y = Distance, fill=Source)) +
  geom_boxplot(outlier.shape = NA) +
  ylim(0,250) + theme_classic() +
  scale_fill_manual(values=brewer.pal(n = 8, 'Set2')) +
  stat_compare_means(aes(group = Source), label = "p.format")
ggsave('prominent_longest/prominent_longest_distance.pdf',width = 8, height = 6,units = 'in',dpi=300)


# Fig 5c
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

ggplot(data = ad, aes(x = Species, y = Count, fill=Species)) +
  geom_bar(stat = 'identity', position = 'dodge', width = 0.5) +
  theme_classic() + scale_fill_manual(values=c('longest'='#EF7F1B', 'truncated'='#1F78AC')) +
  facet_grid(rows = vars(Species))

#Fig 5d
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
## 毕业论文tye 1 2 3 
utype <- read.csv('uORF_ad_type/Archetypal/uORF_utype.csv')
head(utype)
dim(utype)
# type 1 type 3互换，为了画图美观，先小后大
# utype$NewType <- ifelse(utype$Type == "type1", 'type3', ifelse(utype$Type == 'type3', 'type1', 'type2'))
head(utype)
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
pdf("uORF_ad_type/Archetypal/uORF_type123.pdf",width=8,height=6)
p1
dev.off()

## 毕业论文
# ggsave('uORF_ad_type/Archetypal/uORF_type.pdf',width = 8, height = 6,units = 'in',dpi=300)

# 饼图
ggplot(data = utype, aes(x = Species, y = Count, fill=Type)) +
  geom_bar(aes(group = Source, color=Source),stat = 'identity', position = 'dodge', width = 0.5) +
  theme_classic() + scale_fill_manual(values=mypalette) + 
  coord_polar(theta = "y")

  facet_wrap(~Species, scales = 'free') 
  facet_grid(rows = vars(Species), scales = 'free')
  

# Fig 5e
# /home/zhusitao/project/DPI/12.archetypal_truncat_5leader
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/five_UTR_distribution/archetypal_truncate/')
df <- read.csv('five_species_5utr_truncated.csv', header = FALSE)
colnames(df) <- c('Length', 'Species')
head(df)
ggplot(data = df, aes(x = Length, color=Species))+
  geom_density(alpha=0.8) +
  theme_classic() +
  #facet_wrap(~Species) +
  xlim(0,1000) +
  scale_fill_manual(values = brewer.pal(7,"Set2"))
ggsave('archetypal_truncated.pdf',width = 8, height = 6,units = 'in',dpi=300)

# /home/zhusitao/project/DPI/12.archetypal_truncat_5leader
df <- read.csv('Archetypal_longest_truncated.csv')
head(df)
library(plyr)

mu <- ddply(df, .(Species,Source), summarise, grp.median=median(Length))
head(mu)
mu
# facet_grid(rows = vars(Species)) +
# facet_wrap(~Species) +
# facet_wrap(~Species, nrow = 1)
ggplot(data = df, aes(x = Length, fill=Source))+
  geom_density(alpha=0.8) +
  theme_classic() +
  facet_wrap(~Species) +
  xlim(0,1000) +
  geom_vline(data=mu, aes(xintercept=grp.median, color=Species),
             linetype="dashed") +
  ylab('Density') +
  xlab('5\' leader length') + 
  scale_fill_manual(values = brewer.pal(7,"Set2"))
ggsave('Archetypal_longest_truncated.pdf',width = 8, height = 6,units = 'in',dpi=300)

# boxplot
head(df)
ggplot(data = df, aes(x = Species,y = Length, fill=Source)) +
  geom_violin(outlier.shape = NA) + ylim(0,500) + theme_classic()
