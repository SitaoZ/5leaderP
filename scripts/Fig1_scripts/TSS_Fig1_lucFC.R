# LUC Fold Change 
library(ggplot2)
#install.packages("ggpubr")
library(ggpubr)
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/LUC')
df <- read.csv('lucFC_2nd.csv',header = FALSE)
head(df)
dim(df)
colnames(df) <- c('Type','FoldChange')
dim(df)
ggplot(data = df, aes(x = Type, y = FoldChange, color=Type )) +
  geom_boxplot(outlier.shape = NA,width=0.5) +
  geom_jitter(alpha=0.6, width=0.2) +
  ylab(expression(paste("Fold Change of LUC \n against with uORFs_TBF1(483 bp)"))) +
  theme_classic()


ggplot(data = df, aes(x = Type, y = FoldChange, color=Type )) +
  geom_boxplot() +
  geom_jitter(shape=16, position=position_jitter(0.2)) +
  ylab(expression(paste("Fold Change of LUC \n against with uORFs_TBF1(483 bp)"))) +
  theme_classic()

ggplot(data = df, aes(x = Type, y = FoldChange, color=Type )) +
  geom_boxplot() +
  geom_dotplot(binaxis='y', stackdir='center', 
               dotsize=1, aes(fill = Type), 
               alpha = 0.8) +
  ylab(expression(paste("Fold Change of LUC \n against with uORFsTBF1(483bp)"))) +
  theme_classic()

# add p valhe 

# T-test	t.test()	Compare two groups (parametric)
# Wilcoxon test	wilcox.test()	Compare two groups (non-parametric)
# ANOVA	aov() or anova()	Compare multiple groups (parametric)
# Kruskal-Wallis	kruskal.test()	Compare multiple groups (non-parametric)

library(ggpubr)
my_comparisons <- list(c("pSY100", "pSY101"), 
                       c("pSY100", "pSY102"),
                       c("pSY101", "pSY103"),
                       c("pSY102", "pSY103"))

# ggboxplot
ggboxplot(df, x = "Type", y = "FoldChange",
          color = "Type", palette = "aaas",
          width = 0.5,outlier.shape = NA
          ) + 
  stat_compare_means(comparisons = my_comparisons, 
                     label.y = c(2.5, 6.3, 8.0, 7.5), 
                     method = 't.test', aes(label=..p.format..)
                     ) +
  geom_dotplot(binaxis='y', stackdir='center', stackratio=0.5,
               dotsize=0.8, aes(fill = Type), alpha = 0.8, 
               position = position_jitter(0.1), stroke=NA) +
  scale_x_discrete(labels=c("uORFsTBF1(483bp)","uORFsTBF1(372bp)",
                            "uorfsTBF1(483bp)","uorfsTBF1(372bp)")) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        plot.margin = unit(c(1,1,1,1), "cm"),
        legend.position="none") +
  xlab('') +
  ylab(expression(paste("       Fold Change of LUC \n against with uORFsTBF1(483bp)"))) 
ggsave('foldChangeLUC.pdf',width = 8, height = 6,units = 'in',dpi=300)

# ttest check manually 
psy100 <- df[df['Type'] == 'pSY100',]$FoldChange
psy101 <- df[df['Type'] == 'pSY101',]$FoldChange
psy102 <- df[df['Type'] == 'pSY102',]$FoldChange
psy103 <- df[df['Type'] == 'pSY103',]$FoldChange
t.test(psy100, psy101)
t.test(psy100, psy102)
t.test(psy101,psy103)
t.test(psy102, psy103)
#
# two way annova uORF_TBF1(483bp) vs uorf_TBF1(483bp), uORF_TBF1(372bp) uorf_TBF1(372bp)
library(ggpubr)
two_way <- read.csv('uORF_twoway_annova.csv', header = FALSE)
head(two_way)
colnames(two_way) <- c('Type','FoldChange','Length','Upstream')
head(two_way)

str(two_way)
summary(two_way)

# 判断两个因子是否存在交互作用
# 判断是否存在交互，运行结果见图1
# 两条线交叉，说明前面交互作用是显著的。
# 两条线不交叉，说明前面交互作用是不显著的。
interaction.plot(x.factor = two_way$Length,
                 trace.factor = two_way$Upstream,
                 response = two_way$FoldChange,
                 fun = mean,
                 type="b",
                 col=c("black","red","green"),  # Colors for levels of trace var.
                 pch=c(19, 17, 15),             # Symbols for levels of trace var.
                 fixed=TRUE,                    # Order by factor order in data
                 leg.bty = "o")

ggboxplot(two_way,x='Length', y='FoldChange', color = 'Upstream')
ggline(two_way, x='Length', y='FoldChange', color='Upstream',
       add = c("mean_sd"),palette = c("#00AFBB", "#E7B800"),
       legend = "right") +
  geom_dotplot(binaxis='y', stackdir='center', stroke=NA,
               dotsize=0.5, alpha = 0.8, aes(fill=Upstream))+
  ylab('FoldChange of Luciferase') +
  xlab('5 prime leader length' ) 
ggsave('two_anova_uORF_Length.pdf',width = 8, height = 6,units = 'in',dpi=300)


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


# ggline Mean plots
ggline(df, x = "Type", y = "FoldChange",
          color = "Type", palette = "aaas",
          width = 0.5, add = c("mean_se")) + 
  stat_compare_means(comparisons = my_comparisons, 
                     label.y = c(2.3, 2.6, 3.5, 4), method = 't.test') +
  scale_x_discrete(labels=c("uORFsTBF1(483bp)","uORFsTBF1(372bp)","uorfsTBF1(483bp)","uorfsTBF1(372bp)")) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        plot.margin = unit(c(2,1,1,1), "cm"),
        legend.position="none") +
  xlab('') +
  ylab(expression(paste("       Fold Change of LUC \n against with uORFsTBF1(483bp)"))) +
  geom_dotplot(binaxis='y', stackdir='center', 
             dotsize=1, aes(fill = Type), 
             alpha = 0.8) 
