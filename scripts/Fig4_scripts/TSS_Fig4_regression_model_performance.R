# regression model performance 

library(ggplot2)
library(ggpubr)
library(ggprism)
library(ggpmisc)
library(dplyr)
library(rstatix)
getwd()
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/')

### r_square 

# Fig4b
# ath
# /home/zhusitao/AI/TSS_Predict/ath/regression/prediction_interval_fold0.csv
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/')
r_square <- read.csv('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/ath/prediction_interval_fold0.csv')
head(r_square)
tail(r_square)
my.formula <- y ~ x
ggplot(r_square,aes(prediction, true)) +
  geom_point(alpha=0.6,color='black', size=0.8) +
  geom_smooth(method = "lm", se=FALSE, color="black", formula = my.formula) +
  stat_poly_eq(formula = my.formula, 
               aes(label = paste(..eq.label.., ..rr.label.., sep = "~~~"),color='red'), 
               parse = TRUE) +
  xlab("Predicted distance (nt)") +
  ylab("Observed distance (nt)") +
  theme_classic() +
  scale_x_continuous(breaks=seq(0, 256, 100)) +
  scale_y_continuous(breaks=seq(0, 256, 100))
#+ xlim(0,50)
#other way1
summary(lm(prediction ~ true, data=r_square))
#other way2
rsq <- function (x, y) cor(x, y) ^ 2
rsq(r_square$prediction, r_square$true)
ggsave('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/ath/regression_model_r2_ath_0421.pdf',width = 6, height = 6,units = 'in',dpi=300)



# rice
# /home/zhusitao/AI/TSS_Predict/rice/regress/peakCount_tanh/prediction_interval.csv
r_square <- read.csv('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/osa/prediction_interval.csv')
head(r_square)
ggplot(r_square,aes(prediction, true)) +
  geom_point(alpha=0.6,color='black', size=0.8) +
  geom_smooth(method = "lm", se=FALSE, color="black", formula = my.formula) +
  stat_poly_eq(formula = my.formula, 
               aes(label = paste(..eq.label.., ..rr.label.., sep = "~~~"),color='red'), 
               parse = TRUE) +
  xlab("Predicted distance (nt)") +
  ylab("Observed distance (nt)") +
  theme_classic() 
ggsave('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/osa/regression_model_r2_osa.pdf',width = 8, height = 6,units = 'in',dpi=300)

# cotton 
# /home/zhusitao/AI/TSS_Predict/cotton/regress/peakCount_tanh/prediction_interval.csv
r_square <- read.csv('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/gab/prediction_interval.csv')
head(r_square)
ggplot(r_square,aes(prediction, true)) +
  geom_point(alpha=0.6,color='black', size=0.8) +
  geom_smooth(method = "lm", se=FALSE, color="black", formula = my.formula) +
  stat_poly_eq(formula = my.formula, 
               aes(label = paste(..eq.label.., ..rr.label.., sep = "~~~"),color='red'), 
               parse = TRUE) +
  xlab("Predicted distance (nt)") +
  ylab("Observed distance (nt)") +
  theme_classic() 
ggsave('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/gab/regression_model_r2_gab.pdf',width = 8, height = 6,units = 'in',dpi=300)

# maize 
# /home/zhusitao/AI/TSS_Predict/maize/regress/peakCount_tanh/prediction_interval.csv
r_square <- read.csv('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/zma/prediction_interval.csv')
head(r_square)
ggplot(r_square,aes(prediction, true)) +
  geom_point(alpha=0.6,color='black', size=0.8) +
  geom_smooth(method = "lm", se=FALSE, color="black", formula = my.formula) +
  stat_poly_eq(formula = my.formula, 
               aes(label = paste(..eq.label.., ..rr.label.., sep = "~~~"),color='red'), 
               parse = TRUE) +
  xlab("Predicted distance (nt)") +
  ylab("Observed distance (nt)") +
  theme_classic() 
ggsave('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/zma/regression_model_r2_zma.pdf',width = 8, height = 6,units = 'in',dpi=300)

# soybean 
# /home/zhusitao/AI/TSS_Predict/soybean/regress/peakCount_tanh/prediction_interval.csv
r_square <- read.csv('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/gmx/prediction_interval.csv')
head(r_square)
ggplot(r_square,aes(prediction, true)) +
  geom_point(alpha=0.6,color='black', size=0.8) +
  geom_smooth(method = "lm", se=FALSE, color="black", formula = my.formula) +
  stat_poly_eq(formula = my.formula, 
               aes(label = paste(..eq.label.., ..rr.label.., sep = "~~~"),color='red'), 
               parse = TRUE) +
  xlab("Predicted distance (nt)") +
  ylab("Observed distance (nt)") +
  theme_classic() 
ggsave('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/gmx/regression_model_r2_gmx.pdf',width = 8, height = 6,units = 'in',dpi=300)


# Fig4c
# MAE 
MAE <- read.csv('MAE.csv') # 4 models
head(MAE)
MAE_no_plant <- filter(MAE, Species!="plant")
ggplot(data = MAE_no_plant, aes(x=Species, y=MAE)) + 
  geom_boxplot(outlier.shape = NA) + theme_classic() +
  geom_jitter(aes(color=Species, fill=Species), size=3, 
              shape=21, alpha=0.9, width= 0.3, height = 0.3) 
  # stat_boxplot(geom='errorbar', width=0.15)
ggsave('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/MAE_20230421.pdf',width = 8, height = 6,units = 'in',dpi=300)


# Fig4d
# General Plant model
# 总模型的测试集表现
r_square <- read.csv('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/Plant/prediction_interval_fold0.csv')

head(r_square)
my.formula <- y ~ x
ggplot(r_square,aes(prediction, true)) +
  geom_point(alpha=0.6,color='black', size=0.8) +
  geom_smooth(method = "lm", se=FALSE, color="black", formula = my.formula) +
  stat_poly_eq(formula = my.formula, 
               aes(label = paste(..eq.label.., ..rr.label.., sep = "~~~"),color='red'), 
               parse = TRUE) +
  xlab("Predicted distance (nt)") +
  ylab("Observed distance (nt)") +
  theme_classic() 
ggsave('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/Plant/regression_model_r2.pdf',width = 8, height = 6,units = 'in',dpi=300)

