# TSS enrichment
library(ggplot2)
library(reshape2)
library(dplyr)


setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/enrichment_analysis/')

lt05 <- read.csv('rank_lt09_gene_GO_Biological_Process.csv')
# lt05 <- read.csv('/Users/zhusitao/Downloads/enrichment_all (2).csv')
head(lt05)
dim(lt05)
lt05_filter <- filter(lt05, lt05$Enrichment.FDR < 0.05) # 首先根据p值过滤
head(lt05_filter)
dim(lt05_filter)
# 根据显著性排名前18位的
# tmp <- head(arrange(lt05_filter, Enrichment.FDR), 20)
# tmp <- tail(arrange(lt05_filter, Fold.Enrichment), 20) 
tmp <- filter(lt05_filter, Fold.Enrichment >=1 & Enrichment.FDR < 0.05) # 根据p值和富集因子过滤
#tmp <- filter(tmp, grepl('RNA', Pathway)) #只显示RNA代谢相关的，
tmp <- head(arrange(tmp, Enrichment.FDR), 15) # 选取top10画图
tmp$Enrichment.FDR
#tmp %>% filter(grepl('RNA', Pathway)) %>%
tmp %>%
  arrange(Fold.Enrichment) %>%
  mutate(Pathway=factor(Pathway, levels = Pathway)) %>%
  ggplot(aes(x = Fold.Enrichment, y=Pathway)) + 
  geom_point(aes(size=nGenes, color=-log10(Enrichment.FDR))) +
  scale_color_gradient(low = "blue", high = "red") + theme_bw() #+ 
#scale_x_continuous(breaks = c(1.3,1.5,1.7,2), limits = c(1.3,2)) 
ggsave('lt09_GO.pdf',width = 10, height = 10,units = 'in',dpi=300)
