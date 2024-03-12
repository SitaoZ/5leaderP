# Ribo-Seq in five species for uORF in aTSS file 

library(ggplot2)
library(ggsci)
df <- data.frame(Species = c('Arabidopsis', 'Cotton', 'Rice', 'Maize', 'Soybean'), 
                 Ratio = c(0.3619, 0.5366, 0.4510, 0.4998, 0.1618))
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/Ribo_Seq/')
ggplot(data = df, aes(x = Species, y =Ratio, fill = Species)) + 
  geom_bar(stat = 'identity') + theme_classic() + scale_fill_npg() +
  geom_text(aes(label = Ratio), vjust = 1.5, colour = "white") + ylim(0,0.6)
ggsave('aTSS_Ribo_Seq.pdf',width = 8, height = 6,units = 'in',dpi=300)
