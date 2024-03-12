library(ggplot2)
# -------------------------- ath ----------------
# cage tags distribution for read_distribution.py 
# 集群路径
# /home/zhusitao/database/plant/ath/CAGE/readsDistribution.py
# RSeQC
# /home/zhusitao/database/plant/ath/CAGE/reads.txt
getwd()
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/')
# pysradb_downloads_seedings/SRP219883
# RSeQC read_distribution.py
df <- read.csv('reads.txt')
df
ggplot(data = df, aes(x = Sample, y = Tag_count, fill = Group)) +
  geom_col(key_glyph = draw_key_point, position = 'stack', width = 0.6, alpha = 1)+
  theme_classic() +
  guides(fill = guide_legend(
    override.aes=list(shape = 21, size = 5))) +
  scale_fill_brewer(palette = "Paired") +
  labs(x='Sample', y='Tag Count')

# Paired, Set3

library(RColorBrewer)
display.brewer.all()
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/')

# remove paired library 
# /home/zhusitao/database/plant/ath/CAGE/readsDistribution.py
# /home/zhusitao/database/plant/ath/CAGE/reads.txt
# total <- read.csv('reads.txt')
# total <- read.csv('t21.txt') # 除去深度最高的那个样本 比对tair的版本 

# /home/zhusitao/database/plant/ath/CAGE/t21_All_isoform.txt # 比对到All_isoforms.txt版本
# total <- read.csv('t21_All_isoform.txt') 
# total <- read.csv('reads_All_isoform.txt')
total <- read.csv('reads_All_isoform_GeneID.txt')

dim(total)
head(total)
# FigS2a
ggplot(data = total, aes(x = Sample, y = Tag_count, fill = Group)) +
  geom_col(key_glyph = draw_key_point, position = 'stack', width = 0.6, alpha = 1)+
  theme_classic() +
  guides(fill = guide_legend(
    override.aes=list(shape = 21, size = 5))) +
  scale_fill_brewer(palette = "Paired") +
  labs(x='Sample', y='Tag Count') +
  facet_grid(rows = vars(Tissue), scales="free") +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))
# ggsave('cage_tags_distribution_ath.pdf',width = 8, height = 6,units = 'in',dpi=300)
# ggsave('cage_tags_distribution_ath_All_isoform.pdf',width = 8, height = 6,units = 'in',dpi=300)
ggsave('cage_tags_distribution_ath_All_isoform_GeneID.pdf',width = 8, height = 6,units = 'in',dpi=300)


# 密度统计
leaf <- total[total$Tissue=='leaf',]
head(leaf)
# FigS2b
ggplot(data = total, aes(x = Group, y = Tags.Kb, fill=Group)) +
  geom_boxplot() +
  theme_classic() +
  labs(x='Group', y='Tags/Kb') +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))
ggsave('cagetags_density_distribution.pdf',width = 8, height = 6,units = 'in',dpi=300)

# remove outlier 
ggplot(data = total, aes(x = Group, y = Tags.Kb, fill=Group)) +
  geom_boxplot(outlier.shape = NA) +
  theme_classic() +
  labs(x='Group', y='Tags/Kb') +
  ylim(0,100)+
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))
# ggsave('cagetags_density_distribution_remove_outliers.pdf',width = 8, height = 6,units = 'in',dpi=300)
# ggsave('cagetags_density_distribution_remove_outliers_All_isoform.pdf',width = 8, height = 6,units = 'in',dpi=300)
ggsave('cagetags_density_distribution_remove_outliers_All_isoform_GeneID.pdf',width = 8, height = 6,units = 'in',dpi=300)


# ----------------------------- rice -------------------------
# /home/zhusitao/database/plant/rice/CAGE/reads.txt
getwd()
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/')
total <- read.csv('reads_osa.txt')
dim(total)

ggplot(data = total, aes(x = Sample, y = Tag_count, fill = Group)) +
  geom_col(key_glyph = draw_key_point, position = 'stack', width = 0.6, alpha = 1)+
  theme_classic() +
  guides(fill = guide_legend(
    override.aes=list(shape = 21, size = 5))) +
  scale_fill_brewer(palette = "Paired") +
  labs(x='Sample', y='Tag Count') +
  scale_y_continuous(labels = scales::scientific) +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))
ggsave('cage_tags_distribution_osa.pdf',width = 8, height = 6,units = 'in',dpi=300)
#facet_grid(rows = vars(Tissue), scales="free") +

# 密度统计
library(gg.gap)
ggplot(data = total, aes(x = Group, y = Tags.Kb, fill=Group)) +
  geom_boxplot() +
  theme_classic() +
  labs(x='Group', y='Tags/Kb') +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))

p1 <- ggplot(data = total, aes(x = Group, y = Tags.Kb, fill=Group)) +
  geom_boxplot() +
  theme_classic() +
  labs(x='Group', y='Tags/Kb') +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))
p2 <- gg.gap(plot=p1, 
             segments = c(30,80),
             ylim = c(0,125))
ggsave('cagetags_density_distribution_osa.pdf',width = 8, height = 6,units = 'in',dpi=300)

# ------------------------------- cotton ---------------------------
# /home/zhusitao/database/plant/cotton/CAGE/reads.txt
library(ggplot2)
getwd()
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/')
total <- read.csv('reads_gab.txt')
dim(total)

ggplot(data = total, aes(x = Sample, y = Tag_count, fill = Group)) +
  geom_col(key_glyph = draw_key_point, position = 'stack', width = 0.6, alpha = 1)+
  theme_classic() +
  guides(fill = guide_legend(
    override.aes=list(shape = 21, size = 5))) +
  scale_fill_brewer(palette = "Paired") +
  labs(x='Sample', y='Tag Count') +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))

ggsave('cage_tags_distribution_gab.pdf',width = 8, height = 6,units = 'in',dpi=300) 
#facet_grid(rows = vars(Tissue), scales="free") +

# 密度统计
ggplot(data = total, aes(x = Group, y = Tags.Kb, fill=Group)) +
  geom_boxplot() +
  theme_classic() +
  labs(x='Group', y='Tags/Kb') +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))
ggsave('cagetags_density_distribution_gab.pdf',width = 8, height = 6,units = 'in',dpi=300)

# ------------------------- maize -------------------------
# /home/zhusitao/database/plant/maize/CAGE/reads.txt
library(ggplot2)
getwd()
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/')
total <- read.csv('reads_zma.txt')
dim(total)

ggplot(data = total, aes(x = Sample, y = Tag_count, fill = Group)) +
  geom_col(key_glyph = draw_key_point, position = 'stack', width = 0.6, alpha = 1)+
  theme_classic() +
  guides(fill = guide_legend(
    override.aes=list(shape = 21, size = 5))) +
  scale_fill_brewer(palette = "Paired") +
  labs(x='Sample', y='Tag Count') +
  facet_grid(rows = vars(Tissue), scales="free") +
  scale_y_continuous(labels = scales::scientific) +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))

ggsave('cage_tags_distribution_zma.pdf',width = 8, height = 6,units = 'in',dpi=300) 
#facet_grid(rows = vars(Tissue), scales="free") +

# 密度统计
ggplot(data = total, aes(x = Group, y = Tags.Kb, fill=Group)) +
  geom_boxplot() +
  theme_classic() +
  labs(x='Group', y='Tags/Kb') +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))
ggsave('cagetags_density_distribution_zma.pdf',width = 8, height = 6,units = 'in',dpi=300)

# --------------------------------- soybean --------------------------------
# /home/zhusitao/database/plant/soybean/CAGE/reads.txt
library(ggplot2)
getwd()
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/')
total <- read.csv('reads_gmx.txt')
dim(total)

ggplot(data = total, aes(x = Sample, y = Tag_count, fill = Group)) +
  geom_col(key_glyph = draw_key_point, position = 'stack', width = 0.6, alpha = 1)+
  theme_classic() +
  guides(fill = guide_legend(
    override.aes=list(shape = 21, size = 5))) +
  scale_fill_brewer(palette = "Paired") +
  labs(x='Sample', y='Tag Count') +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))

ggsave('cage_tags_distribution_gmx.pdf',width = 8, height = 6,units = 'in',dpi=300) 
#facet_grid(rows = vars(Tissue), scales="free") +

# 密度统计
ggplot(data = total, aes(x = Group, y = Tags.Kb, fill=Group)) +
  geom_boxplot() +
  theme_classic() +
  labs(x='Group', y='Tags/Kb') +
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=1))
ggsave('cagetags_density_distribution_gmx.pdf',width = 8, height = 6,units = 'in',dpi=300)
