# five species UTR length 
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

