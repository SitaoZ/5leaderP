# five species UTR length 
library(ggplot2)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/five_UTR_distribution/')

# /home/zhusitao/database/plant/rice/MSU7/create/five_species_5utr.csv
df <- read.csv('five_species_5utr.csv', header = FALSE)

head(df)
colnames(df) <- c('utr5', 'species')
head(df)
dim(df)

library(plyr)
mu <- ddply(df, "species", summarise, grp.mean=mean(utr5))
head(mu)
mu

#### color brewer
library(RColorBrewer)
?RColorBrewer
display.brewer.all(n=NULL, type="all", select=NULL, exact.n=TRUE, 
                   colorblindFriendly=FALSE)
mypalette <- brewer.pal(7,"Set2")

ggplot(data = df, aes(x = utr5, fill=species))+
  geom_density(alpha=0.8) +
  theme_classic() +
  facet_grid(rows = vars(species)) +
  xlim(0,1000) +
  geom_vline(data=mu, aes(xintercept=grp.mean, color=species),
              linetype="dashed") +
  ylab('Density') +
  xlab('5\' UTR length') 
ggsave('Input_threshold.pdf',width = 8, height = 6,units = 'in',dpi=300)

# 和注释前后的gtf版本比较5leader的分布情况，看前后变化
# 第二组装版本 (ath_inherit_correct.gff)
# /home/zhusitao/database/plant/rice/MSU7/create/UTR5/five_species_5utr_reference_vs_assemble.csv
# 第一组装版本(transdecoder.gff3)
# ll /home/zhusitao/database/plant/*/merge_gff/04.decoder/transdecoder/create/*5utr_assemble.csv

# 目前采用第三组装版本 All_isoforms_V1.0.gff
# ls -lth  /home/zhusitao/database/plant/*/merge_gff/01.merge/mani/gff_inherit/All_Archetypal_isoforms_Arabidopsis_V1.0/create/*5utr_assemble.csv
# /home/zhusitao/database/plant/ath/merge_gff/01.merge/current/mani/gff_inherit/All_Archetypal_isoforms_Arabidopsis_V1.0/create/five_prime_length_distribution
library(ggplot2)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/five_UTR_distribution/')

df <- read.csv('five_species_5utr_reference_vs_assemble.csv', header = FALSE)

head(df)
colnames(df) <- c('utr5', 'version','species')
head(df)
dim(df)

library(plyr)
# mu <- ddply(df, .(species,version), summarise, grp.mean=mean(utr5))
mu <- ddply(df, .(species,version), summarise, grp.median=median(utr5))
head(mu)
mu

#### color brewer
library(RColorBrewer)
?RColorBrewer
display.brewer.all(n=NULL, type="all", select=NULL, exact.n=TRUE, 
                   colorblindFriendly=FALSE)
mypalette <- brewer.pal(10,"Paired")

ggplot(data = df, aes(x = utr5, fill=version))+
  geom_density(alpha=0.8) +
  theme_classic() +
  facet_grid(rows = vars(species)) +
  xlim(0,1000) +
  geom_vline(data=mu, aes(xintercept=grp.median, color=species),
             linetype="dashed") +
  ylab('Density') +
  xlab('5\' leader length') +
  scale_fill_manual(values = mypalette)
ggsave('Input_threshold_reference_vs_assemble.pdf',width = 8, height = 6,units = 'in',dpi=300)

# facet_grid(rows = vars(species)) +
ggplot(data = df, aes(x = utr5, fill=version))+
  geom_density(alpha=0.8) +
  theme_classic() +
  facet_wrap(~species) +
  xlim(0,1000) +
  geom_vline(data=mu, aes(xintercept=grp.median, color=species),
             linetype="dashed") +
  ylab('Density') +
  xlab('5\' leader length') + 
  scale_fill_manual(values = mypalette)
ggsave('Input_threshold_reference_vs_assemble_wrap.pdf',width = 8, height = 6,units = 'in',dpi=300)



# Fig5d
# 截断之后的archetypal转录本的长度分布

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

df <- read.csv('Archetypal_longest_truncated.csv')
head(df)
library(plyr)

mu <- ddply(df, .(Species,Source), summarise, grp.median=median(Length))
head(mu)
mu

ggplot(data = df, aes(x = Length, fill=Source))+
  geom_density(alpha=0.8) +
  theme_classic() +
  facet_grid(rows = vars(Species)) +
  xlim(0,1000) +
  scale_fill_manual(values = brewer.pal(7,"Set2"))
ggsave('Archetypal_longest_truncated.pdf',width = 8, height = 6,units = 'in',dpi=300)