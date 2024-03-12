#Robust and Permissive peak region length distributation 
library(ggplot2)
library(dplyr)

setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/')

# ---------------------------------ath #
# bed 文件格式是0-based的，所以计算长度使用的是end - start
# 这一点和1-based的文件(如 GFF)是有不同的，它们使用的是end - start + 1
# 详情见https://en.wikipedia.org/wiki/BED_(file_format)
# /home/zhusitao/project/DPI/01.ath/peak_process/02.bed2gff/robust_peak_length.csv
# /home/zhusitao/project/DPI/01.ath/peak_process/07.permissive/permissive_peak_length.csv
robust_peak <- read.csv('ath/robust_peak_length.csv', header = 0)
head(robust_peak)
dim(robust_peak)
colnames(robust_peak) <- 'Peak_Length'
robust_peak['Type'] <- 'robust'
head(robust_peak)

permissive_peak <- read.csv('ath/permissive_peak_length.csv', header = 0)
head(permissive_peak)
dim(permissive_peak)
colnames(permissive_peak) <- 'Peak_Length'
permissive_peak['Type'] <- 'permissive'
head(permissive_peak)

ath_peak <- rbind(robust_peak, permissive_peak)
ath_peak['species'] <- 'ath'
head(ath_peak)
ath_median <- summarise(group_by(ath_peak, Type), MD = median(Peak_Length))
ath_median

ggplot(data = ath_peak, aes(x = Type, y = Peak_Length, color = Type)) + 
  geom_boxplot(outlier.shape = NA) +
  lims(y = c(0,100)) +
  labs(x = 'Peak Type', y = 'Peak Length') +
  geom_text(data = ath_median, aes(Type, MD, label = MD),
            position = position_dodge(width = 0.8), size = 3, vjust = -0.5) + 
  theme_classic()
ggsave('ath/ath_peak_length.pdf',width = 8, height = 6,units = 'in',dpi=300)


# ---------------------------------osa #
# /home/zhusitao/project/DPI/01.osa/peak_process/02.bed2gff/robust_peak_length.csv
# /home/zhusitao/project/DPI/01.osa/peak_process/07.permissive/permissive_peak_length.csv
robust_peak <- read.csv('osa/robust_peak_length.csv', header = 0)
head(robust_peak)
dim(robust_peak)
colnames(robust_peak) <- 'Peak_Length'
robust_peak['Type'] <- 'robust'
head(robust_peak)

permissive_peak <- read.csv('osa/permissive_peak_length.csv', header = 0)
head(permissive_peak)
dim(permissive_peak)
colnames(permissive_peak) <- 'Peak_Length'
permissive_peak['Type'] <- 'permissive'
head(permissive_peak)

osa_peak <- rbind(robust_peak, permissive_peak)
osa_peak['species'] <- 'osa'
head(osa_peak)
osa_median <- summarise(group_by(osa_peak, Type), MD = median(Peak_Length))
osa_median

ggplot(data = osa_peak, aes(x = Type, y = Peak_Length, color = Type)) + 
  geom_boxplot(outlier.shape = NA) +
  lims(y = c(0,100)) +
  labs(x = 'Peak Type', y = 'Peak Length') +
  geom_text(data = osa_median, aes(Type, MD, label = MD),
            position = position_dodge(width = 0.8), size = 3, vjust = -0.5) + 
  theme_classic()
ggsave('osa/osa_peak_length.pdf',width = 8, height = 6,units = 'in',dpi=300)


# ---------------------------------gab #
# /home/zhusitao/project/DPI/01.gab/peak_process/02.bed2gff/robust_peak_length.csv
# /home/zhusitao/project/DPI/01.gab/peak_process/07.permissive/permissive_peak_length.csv
robust_peak <- read.csv('gab/robust_peak_length.csv', header = 0)
head(robust_peak)
dim(robust_peak)
colnames(robust_peak) <- 'Peak_Length'
robust_peak['Type'] <- 'robust'
head(robust_peak)

permissive_peak <- read.csv('gab/permissive_peak_length.csv', header = 0)
head(permissive_peak)
dim(permissive_peak)
colnames(permissive_peak) <- 'Peak_Length'
permissive_peak['Type'] <- 'permissive'
head(permissive_peak)

gab_peak <- rbind(robust_peak, permissive_peak)
gab_peak['species'] <- 'gab'
head(gab_peak)
gab_median <- summarise(group_by(gab_peak, Type), MD = median(Peak_Length))
gab_median

ggplot(data = gab_peak, aes(x = Type, y = Peak_Length, color = Type)) + 
  geom_boxplot(outlier.shape = NA) +
  lims(y = c(0,100)) +
  labs(x = 'Peak Type', y = 'Peak Length') +
  geom_text(data = gab_median, aes(Type, MD, label = MD),
            position = position_dodge(width = 0.8), size = 3, vjust = -0.5) + 
  theme_classic()
ggsave('gab/gab_peak_length.pdf',width = 8, height = 6,units = 'in',dpi=300)


# ---------------------------------zma #
# /home/zhusitao/project/DPI/04.zma/peak_process/02.bed2gff/robust_peak_length.csv
# /home/zhusitao/project/DPI/04.zma/peak_process/07.permissive/permissive_peak_length.csv
robust_peak <- read.csv('zma/robust_peak_length.csv', header = 0)
head(robust_peak)
dim(robust_peak)
colnames(robust_peak) <- 'Peak_Length'
robust_peak['Type'] <- 'robust'
head(robust_peak)

permissive_peak <- read.csv('zma/permissive_peak_length.csv', header = 0)
head(permissive_peak)
dim(permissive_peak)
colnames(permissive_peak) <- 'Peak_Length'
permissive_peak['Type'] <- 'permissive'
head(permissive_peak)

zma_peak <- rbind(robust_peak, permissive_peak)
zma_peak['species'] <- 'zma'
head(zma_peak)
zma_median <- summarise(group_by(zma_peak, Type), MD = median(Peak_Length))
zma_median

ggplot(data = zma_peak, aes(x = Type, y = Peak_Length, color = Type)) + 
  geom_boxplot(outlier.shape = NA) +
  lims(y = c(0,100)) +
  labs(x = 'Peak Type', y = 'Peak Length') +
  geom_text(data = zma_median, aes(Type, MD, label = MD),
            position = position_dodge(width = 0.8), size = 3, vjust = -0.5) + 
  theme_classic()
ggsave('zma/zma_peak_length.pdf',width = 8, height = 6,units = 'in',dpi=300)


# ---------------------------------gmx #
# /home/zhusitao/project/DPI/05.gmx/peak_process/02.bed2gff/robust_peak_length.csv
# /home/zhusitao/project/DPI/05.gmx/peak_process/07.permissive/permissive_peak_length.csv
robust_peak <- read.csv('gmx/robust_peak_length.csv', header = 0)
head(robust_peak)
dim(robust_peak)
colnames(robust_peak) <- 'Peak_Length'
robust_peak['Type'] <- 'robust'
head(robust_peak)

permissive_peak <- read.csv('gmx/permissive_peak_length.csv', header = 0)
head(permissive_peak)
dim(permissive_peak)
colnames(permissive_peak) <- 'Peak_Length'
permissive_peak['Type'] <- 'permissive'
head(permissive_peak)

gmx_peak <- rbind(robust_peak, permissive_peak)
gmx_peak['species'] <- 'gmx'
head(gmx_peak)
gmx_median <- summarise(group_by(gmx_peak, Type), MD = median(Peak_Length))
gmx_median

ggplot(data = gmx_peak, aes(x = Type, y = Peak_Length, color = Type)) + 
  geom_boxplot(outlier.shape = NA) +
  lims(y = c(0,100)) +
  labs(x = 'Peak Type', y = 'Peak Length') +
  geom_text(data = gmx_median, aes(Type, MD, label = MD),
            position = position_dodge(width = 0.8), size = 3, vjust = -0.5) + 
  theme_classic()
ggsave('gmx/gmx_peak_length.pdf',width = 8, height = 6,units = 'in',dpi=300)




#### merge five species #####

total_peak <- rbind(ath_peak, osa_peak, gab_peak, zma_peak, gmx_peak)
dim(ath_peak)
dim(osa_peak)
dim(gab_peak)
dim(zma_peak)
dim(gmx_peak)
dim(total_peak)
head(total_peak)

library(plyr)
total_median <- ddply(total_peak, .(Type,species), summarise, grp.median=median(Peak_Length))
head(total_median)
total_median

library(RColorBrewer)
?RColorBrewer
display.brewer.all(n=NULL, type="all", select=NULL, exact.n=TRUE, 
                   colorblindFriendly=FALSE)
mypalette <- brewer.pal(10,"Paired")

ggplot(data = total_peak, aes(x = species, y = Peak_Length,fill=species, color = Type)) + 
  geom_boxplot(outlier.shape = NA) +
  lims(y = c(0,50)) +
  labs(x = 'Species', y = 'Peak Length') +
  scale_fill_manual(values = mypalette) +
  geom_text(data = total_median, aes(species, grp.median, label = grp.median),
            position = position_dodge(width = 0.75), size = 3, vjust = 0.5 , hjust=-0.5) + 
  theme_classic()

ggsave('five_species_peak_length.pdf',width = 8, height = 6,units = 'in',dpi=300)

# 对齐有问题，所以原图不放median，附件图中放median
ggplot(data = total_peak, aes(x = species, y = Peak_Length,fill=species, color = Type)) + 
  geom_boxplot(outlier.shape = NA) +
  lims(y = c(0,50)) +
  labs(x = 'Species', y = 'Peak Length') +
  scale_fill_manual(values = mypalette) +
  theme_classic()
ggsave('five_species_peak_length_no_median.pdf',width = 8, height = 6,units = 'in',dpi=300)



# Fantom six species distributation 
# /home/zhusitao/AI/Fantom/TSS_Classifier 
library(ggplot2)
library(RColorBrewer)
library(plyr)


mypalette <- brewer.pal(10,"Set1")
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/')
df <- read.csv('Fantom/fantom_six_species_permissive_length.csv', header = FALSE)
colnames(df) <- c('Species', 'Length')
head(df)
df_median <- ddply(df, .(Species), summarise, grp.median=median(Length))
head(df_median)
df_median

ggplot(data = df, aes(x = Species, y = Length, fill=Species)) + 
  geom_boxplot(outlier.shape = NA) +
  lims(y = c(0,50)) +
  labs(x = 'Species', y = 'Peak Length') +
  scale_fill_manual(values = mypalette) +
  theme_classic() +
  geom_text(data = df_median, aes(Species, grp.median, label = grp.median),
            position = position_dodge(width = 0.75), size = 3, vjust = 0.5 , hjust=-0.5) 
ggsave('Fantom/six_species_peak_length_median.pdf',width = 8, height = 6,units = 'in',dpi=300)
