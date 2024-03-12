# LUC Fold Change 
library(ggplot2)
#install.packages("ggpubr")
library(ggpubr)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/LUC')


# two way annova uORF_TBF1(483bp) vs uorf_TBF1(483bp), uORF_TBF1(372bp) uorf_TBF1(372bp)
two_way <- read.csv('uORF_twoway_annova.csv', header = FALSE)
head(two_way)
colnames(two_way) <- c('Type','FoldChange','Length','Upstream')
head(two_way)
str(two_way)
summary(two_way)

# two-way anova figure (for pub) current version
ggbarplot(two_way, x = "Length", y = "FoldChange", color = 'Upstream', palette = "aaas",
          add = c("mean_sd"), position = position_dodge(width = NULL)) +
  geom_dotplot(stackratio=0.31,binaxis='y',
               dotsize=0.8, alpha = 0.8, aes(fill = Upstream),
               position = position_jitterdodge(jitter.width = 0.2,
                                               jitter.height = 0.2,
                                               dodge.width = 0.75), 
               stroke=NA) + 
  theme(axis.text.x = element_text(angle = 0, hjust = 1),
        plot.margin = unit(c(1,1,1,1), "cm"),
        legend.position="right") +
  stat_compare_means(aes(label = ..p.format..), method = "anova", label.y = 7, 
                     symnum.args = list(cutpoints = c(0, 0.0001, 0.001, 0.01, 0.05, 1),
                                        symbols = c("****", "***", "**", "*", "NS"))) +
  ylab(expression(paste("LUC activity"))) 

ggsave('foldChangeLUC_twoWay_anova.pdf',width = 8, height = 6,units = 'in',dpi=300)


# two-way annovar
# res.aov2 <- aov(FoldChange ~ uORF + Length, data = two_way)
res.aov2 <- aov(FoldChange ~ Upstream + Length, data = two_way)
summary(res.aov2)

#                 Df Sum Sq Mean Sq F value   Pr(>F)    
#  uORF          1 294.41  294.41  366.44  < 2e-16 ***
#  Length        1  42.21   42.21   52.54 4.91e-11 ***
#  Residuals   117  94.00    0.80                     
#  ---
#  Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

# 这个结果是加性模型，additive model，表示uORF和Length是相互独立的两个因子。
# 用的是+号
# 从结果中可以知道长度和uORF对FoldChange的影响都是显著的，
# uORF是最显著的影响因素。说明改变uORF和长度都能影响FoldChange。
# 

# two-way annovar with interaction 如果两个因子之间不独立，又相互作用
# +号变成*号，replace plus (+) symbol by asterisk(*).
res.aov3 <- aov(FoldChange ~ uORF * Length, data = two_way)
summary(res.aov3)
#             Df Sum Sq Mean Sq F value   Pr(>F)    
#uORF          1 294.41  294.41  426.27  < 2e-16 ***
#  Length        1  42.21   42.21   61.11 2.71e-12 ***
#  uORF:Length   1  13.88   13.88   20.10 1.73e-05 ***
#  Residuals   116  80.12    0.69                     
#---
#  Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 可以看出，不仅uORF和Length对FoldChange的影响是显著的，它们之间的相互作用的影响也是显著的。
