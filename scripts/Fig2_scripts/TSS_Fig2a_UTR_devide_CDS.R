# UTR/CDS
# reference vs assemble in five species
library(ggplot2)
library(ggpubr)
library(reshape2)
library(ggsci)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/UTR_devide_CDS/')
# /home/zhusitao/database/plant/ath/merge_gff/01.merge/current/mani/gff_inherit/All_Archetypal_isoforms_Arabidopsis_V1.0/UTR_devide_CDS/get_utr5_utr3_devide_cds.py
ath <- read.csv('ath_utr53_devide_cds_refer.csv')
head(ath)


# 比价reference 和 assembly
ath_comp <- read.csv('ath_utr53_devide_cds_refer_assem.csv')
head(ath_comp)
ath_melt <- melt(ath_comp)
head(ath_melt)
ggplot(data = ath_melt, aes(x = variable, y = value, fill=variable)) +
  geom_boxplot(outlier.shape = NA) + ylim(0,0.6) +
  theme_classic() + scale_fill_npg() + stat_compare_means(method = "t.test")

ath$Species <- 'arabidopsis'
head(ath)
df1 <- subset(ath, select = c("LenRatioRefer", "Species"))
head(df1)

osa <- read.csv('osa_utr53_devide_cds.csv')
osa$Species <- 'rice'
df2 <- subset(osa, select = c("LenRatioRefer", "Species"))
head(df2)

gab <- read.csv('gab_utr53_devide_cds.csv')
gab$Species <- 'cotton'
df3 <- subset(gab, select = c("LenRatioRefer", "Species"))
head(df3)

zma <- read.csv('zma_utr53_devide_cds.csv')
zma$Species <- 'maize'
df4 <- subset(zma, select = c("LenRatioRefer", "Species"))
head(df4)

gmx <- read.csv('gmx_utr53_devide_cds.csv')
gmx$Species <- 'soybean'
df5 <- subset(gmx, select = c("LenRatioRefer", "Species"))
head(df5)
# df6 用于测试
#df6 <- read.csv('gmx_utr_devide_cds3.csv')
#df6$Species <- 'XXX'
#df6 <- subset(df6, select = c("LenRatioRefer", "Species"))

df <- rbind(df1, df2, df3, df4, df5)
head(df)
tail(df)
# library(ggsci)
# nature 配色 scale_color_npg scale_fill_npg
# science 配色 scale_color_aaas scale_fill_aaas
# Lancet 配色 scale_color_lancet scale_fill_lancet
ggplot(data = df, aes(x = Species, y = LenRatioRefer, fill=Species)) +
  geom_boxplot(outlier.shape = NA) + ylim(0,0.2) +
  theme_classic() + scale_fill_npg() + 
  geom_hline(aes(yintercept=0.05),linetype='dotted') +
  ylab("Length ratio (5'leader/CDS)") +
  stat_compare_means(method = "anova")

ggsave('species_UTR_devide_CDS.pdf',width = 8, height = 6,units = 'in',dpi=300)
# species_UTR_devide_CDS_abs.pdf 是绝对值，species_UTR_devide_CDS.pdf是密度


# assembly 
ath <- read.csv('ath_utr53_devide_cds_assem.csv')
ath$Species <- 'arabidopsis'
df1 <- subset(ath, select = c("LenRatioAssem", "Species"))
head(df1)

osa <- read.csv('osa_utr53_devide_cds_assem.csv')
osa$Species <- 'rice'
df2 <- subset(osa, select = c("LenRatioAssem", "Species"))
head(df2)

gab <- read.csv('gab_utr53_devide_cds_assem.csv')
gab$Species <- 'cotton'
df3 <- subset(gab, select = c("LenRatioAssem", "Species"))
head(df3)

zma <- read.csv('zma_utr53_devide_cds_assem.csv')
zma$Species <- 'maize'
df4 <- subset(zma, select = c("LenRatioAssem", "Species"))
head(df4)

gmx <- read.csv('gmx_utr53_devide_cds_assem.csv')
gmx$Species <- 'soybean'
df5 <- subset(gmx, select = c("LenRatioAssem", "Species"))
head(df5)

df <- rbind(df1, df2, df3, df4, df5)
head(df)
tail(df)
ggplot(data = df, aes(x = Species, y = LenRatioAssem, fill=Species)) +
  geom_boxplot(outlier.shape = NA) + ylim(0,0.2) +
  theme_classic() + scale_fill_npg() + 
  geom_hline(aes(yintercept=0.05),linetype='dotted') +
  ylab("Length ratio (5'leader/CDS)") +
  stat_compare_means(method = "anova")

ggsave('species_UTR_devide_CDS_Assembly.pdf',width = 8, height = 6,units = 'in',dpi=300)

# merge total map 
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/UTR_devide_CDS/')
ath <- read.csv('ath_utr53_devide_cds_refer_assem.csv')
head(ath)
ath_melt <- melt(ath, id=c('TranscriptID'), variable.name="Type", value.name="Ratio")
head(ath_melt)
ath_melt$Species <- 'arabidopsis'
df1 <- subset(ath_melt, select = c("Type", "Ratio", "Species"))
head(df1)

osa <- read.csv('osa_utr53_devide_cds_refer_assem.csv')
osa_melt <- melt(osa, id=c('TranscriptID'), variable.name="Type", value.name="Ratio")
osa_melt$Species <- 'rice'
df2 <- subset(osa_melt, select = c("Type", "Ratio", "Species"))
head(df2)

gab <- read.csv('gab_utr53_devide_cds_refer_assem.csv')
gab_melt <- melt(gab, id=c('TranscriptID'), variable.name="Type", value.name="Ratio")
gab_melt$Species <- 'cotton'
df3 <- subset(gab_melt, select = c("Type", "Ratio", "Species"))
head(df3)

zma <- read.csv('zma_utr53_devide_cds_refer_assem.csv')
zma_melt <- melt(zma, id=c('TranscriptID'), variable.name="Type", value.name="Ratio")
zma_melt$Species <- 'maize'
df4 <- subset(zma_melt, select = c("Type", "Ratio", "Species"))
head(df4)

gmx <- read.csv('gmx_utr53_devide_cds_refer_assem.csv')
gmx_melt <- melt(gmx, id=c('TranscriptID'), variable.name="Type", value.name="Ratio")
gmx_melt$Species <- 'soybean'
df5 <- subset(gmx_melt, select = c("Type", "Ratio", "Species"))
head(df5)

df <- rbind(df1, df2, df3, df4, df5)
head(df)
tail(df)
df$Log_Ratio <- log2(df$Ratio)
# ylim(0,0.25)
ggplot(data = df, aes(x = Species, y = Ratio, color = Type)) +
  geom_boxplot(outlier.shape = NA) + ylim(0,0.25) +
  theme_classic() + scale_color_npg() + 
  geom_hline(aes(yintercept=0.05),linetype='dotted') +
  ylab("Log2 of Length ratio (5'leader/CDS)") +
  stat_compare_means(aes(label = ..p.format..), method = "anova", label.y = 0.24, 
                     symnum.args = list(cutpoints = c(0, 0.0001, 0.001, 0.01, 0.05, 1),
                                        symbols = c("****", "***", "**", "*", "NS")))
ggsave('species_UTR_devide_CDS_total.pdf',width = 8, height = 6,units = 'in',dpi=300)

# log2
# scale_y_continuous(breaks =seq(-15, 5, 5), limit = c(-10, 1)) 不影响数据分布
ggplot(data = df, aes(x = Species, y = Log_Ratio, fill = Type)) +
  geom_boxplot(outlier.shape = NA) + 
  scale_y_continuous(breaks =seq(-15, 5, 5), limit = c(-10, 1)) + 
  theme_classic() + scale_fill_npg() + 
  geom_hline(aes(yintercept=-3.82),linetype='dotted') +
  ylab("Log2 of Length ratio (5'leader/CDS)") +
  stat_compare_means(aes(label = ..p.format..), method = "anova", label.y = 0.24, 
                     symnum.args = list(cutpoints = c(0, 0.0001, 0.001, 0.01, 0.05, 1),
                                        symbols = c("****", "***", "**", "*", "NS")))

#
# More than two groups
#:::::::::::::::::::::::::::::::::::::::::::::::::
# Pairwise comparisons: Specify the comparisons you want
library(dplyr)
a <- filter(df, Type == "LenRatioRefer" & Species == 'arabidopsis')
median(a$Log_Ratio)
ggboxplot(df, x = "Species", y = "Log_Ratio",
          color = "Type", palette = "npg", outlier.shape=NA) +
  geom_hline(aes(yintercept=-3.82),linetype='dotted') +
  scale_y_continuous(breaks =seq(-15, 5, 5), limit = c(-10, 1)) +
  ylab("Log2 of Length ratio (5'leader/CDS)")
  

#
anova <- aov(Log_Ratio ~ Species*Type, data = df)
summary(anova)

ggsave('species_UTR_devide_CDS_log_total.pdf',width = 8, height = 6,units = 'in',dpi=300)

# 和动物比较
# animal
# hsa
hsa <- read.csv('hsa_utr53_devide_cds_refer.csv')
hsa$Species <- 'B1_Human'
head(hsa)
#dme
dme <- read.csv('dme_utr53_devide_cds_refer.csv')
dme$Species <- 'B4_Drosophila'
head(dme)
#mouse 
mmu <- read.csv('mmu_utr53_devide_cds_refer.csv')
mmu$Species <- 'B2_Mouse'
head(mmu)
# zebrafish 
dre <- read.csv('dre_utr53_devide_cds_refer.csv')
dre$Species <- 'B3_Zebrafish'
head(dre)

# cel
cel <- read.csv('cel_utr53_devide_cds_refer.csv')
cel$Species <- 'B5_Elegans'
head(cel)


ath <- read.csv('ath_utr53_devide_cds_refer.csv')
ath$Species <- 'A1_Arabidopsis'

osa <- read.csv('osa_utr53_devide_cds.csv')
osa$Species <- 'A4_Rice'

gab <- read.csv('gab_utr53_devide_cds.csv')
gab$Species <- 'A2_cotton'

zma <- read.csv('zma_utr53_devide_cds.csv')
zma$Species <- 'A3_Maize'

gmx <- read.csv('gmx_utr53_devide_cds.csv')
gmx$Species <- 'A5_Soybean'

sor <- read.csv('sor_utr53_devide_cds_refer.csv')
sor$Species <- 'A6_sorghum'

sor2 <- read.csv('sor_tx436_utr53_devide_cds_refer.csv')
sor2$Species <- 'A7_sorghum'

svi <- read.csv('svi_utr53_devide_cds_refer.csv')
svi$Species <- 'A8_Sevir'
library(RColorBrewer)
mypalette <- brewer.pal(7,"Set1")
display.brewer.all(n=NULL, type="all", select=NULL, exact.n=TRUE, 
                   colorblindFriendly=FALSE)
comp <- rbind(ath, osa, gab, zma, gmx, sor, sor2, svi, hsa, dme, dre,mmu, cel)
ggplot(data = comp, aes(x = Species, y = LenRatioRefer, fill=Species)) +
  geom_boxplot(outlier.shape = NA) + ylim(0,0.3) +
  theme_classic() + scale_fill_manual(values=terrain.colors(13)) +
  stat_compare_means(method = "anova")
ggsave('plant_animal_UTR_devide_CDS_.pdf',width = 8, height = 6,units = 'in',dpi=300)

#+ scale_fill_npg() 
#+ scale_fill_brewer(palette = 'Set3')
# terrain.colors(13)
# cm.colors(13)

# 只计算含有uORF的转录本---------------------------------------
ath <- read.csv('uORF/ath_utr53_devide_cds_uORF.csv')
ath$Species <- 'arabidopsis'
df1 <- subset(ath, select = c("LenRatioRefer", "Species"))

osa <- read.csv('uORF/osa_utr53_devide_cds_uORF.csv')
osa$Species <- 'rice'
df2 <- subset(osa, select = c("LenRatioRefer", "Species"))

gab <- read.csv('uORF/gab_utr53_devide_cds_uORF.csv')
gab$Species <- 'cotton'
df3 <- subset(gab, select = c("LenRatioRefer", "Species"))

zma <- read.csv('uORF/zma_utr53_devide_cds_uORF.csv')
zma$Species <- 'maize'
df4 <- subset(zma, select = c("LenRatioRefer", "Species"))

gmx <- read.csv('uORF/gmx_utr53_devide_cds_uORF.csv')
gmx$Species <- 'soybean'
df5 <- subset(gmx, select = c("LenRatioRefer", "Species"))

df <- rbind(df1, df2, df3, df4, df5)
ggplot(data = df, aes(x = Species, y = LenRatioRefer, fill=Species)) +
  geom_boxplot(outlier.shape = NA) + ylim(0,0.75) +
  theme_classic() + scale_fill_npg() + geom_hline(aes(yintercept=0.15))
