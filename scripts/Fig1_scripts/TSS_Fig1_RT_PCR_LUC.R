#TSS RT-PCR of LUC
library(ggplot2)
#install.packages("ggpubr")
library(ggpubr)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/LUC')
# df <- read.csv('lucRT.csv',header = FALSE)
# df <- read.csv('lucRT_add_attr.csv', header = FALSE) # raw ,不知道怎么处理的，居然有5个点
df <- read.csv('lucRT_20230629.csv', header = FALSE)
head(df)
dim(df)
colnames(df) <- c('Type','FoldChange','Length','Upstream')
dim(df)
head(df)
ggplot(data = df, aes(x = Type, y = FoldChange, color=Type )) +
  geom_boxplot(outlier.shape = NA,width=0.5) +
  geom_jitter(alpha=0.6, width=0.2) +
  ylab(expression(paste("Fold Change of LUC \n against with uORFs_TBF1(483 bp)"))) +
  theme_classic()

library(ggpubr)
my_comparisons <- list(c("pSY100", "pSY101"), 
                       c("pSY100", "pSY102"),
                       c("pSY101", "pSY103"),
                       c("pSY102", "pSY103"))

# ggbarplot
# 两组或者多组的均值比较，用卡方检验
ggbarplot(df, x = "Type", y = "FoldChange",
          color = "Type", palette = "aaas",
          width = 0.5,
          add = "mean_sd", error.plot = "errorbar"
          ) + 
  stat_compare_means(method = 'anova', label.y = 4) + 
  stat_compare_means(ref.group = '.all.', method = 't.test', label="p.signif") +
  geom_dotplot(binaxis='y', stackdir='center', stackratio=0.5,
               dotsize=1, aes(fill = Type), alpha = 0.8, 
               position = position_jitter(0.1), stroke=NA) +
  scale_x_discrete(labels=c("uORFsTBF1(483bp)","uORFsTBF1(372bp)",
                            "uorfsTBF1(483bp)","uorfsTBF1(372bp)")) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        plot.margin = unit(c(1,1,1,1), "cm"),
        legend.position="none") +
  xlab('') +
  ylab(expression(paste("LUC/Basta mRNA level"))) 

# 使用的数据是2023-03-25-2nd的结果，是生物学重复
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
