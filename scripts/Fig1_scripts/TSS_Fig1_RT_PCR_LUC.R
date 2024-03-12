#TSS RT-PCR of LUC
library(ggplot2)
#install.packages("ggpubr")
library(ggpubr)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/LUC')
df <- read.csv('lucRT_20230629.csv', header = FALSE)
head(df)
dim(df)
colnames(df) <- c('Type','FoldChange','Length','Upstream')
dim(df)
head(df)

## 2023,06,29 version,使用normalize版本，之前使用的相对含量的数据
ggbarplot(df, x = "Length", y = "FoldChange", color = 'Upstream', palette = "aaas",
          add = c("mean_sd"), position = position_dodge(width = NULL)) +
  geom_dotplot(stackratio=0.31,binaxis='y',
               dotsize=0.8, alpha = 0.8, aes(fill = Upstream),
               position = position_jitterdodge(jitter.width = 0.2,
                                               jitter.height = 0,
                                               dodge.width = 0.75), 
               stroke=NA) + 
  theme(axis.text.x = element_text(angle = 0, hjust = 1),
        plot.margin = unit(c(1,1,1,1), "cm"),
        legend.position="right") +
  stat_compare_means(aes(label = ..p.format..), method = "anova", label.y = 2, 
                     symnum.args = list(cutpoints = c(0, 0.0001, 0.001, 0.01, 0.05, 1),
                                        symbols = c("****", "***", "**", "*", "NS"))) +
  ylab(expression(paste("LUC/Basta mRNA level"))) 

ggsave('LUC_Basta_RT_PCR.pdf',width = 8, height = 6,units = 'in',dpi=300)
