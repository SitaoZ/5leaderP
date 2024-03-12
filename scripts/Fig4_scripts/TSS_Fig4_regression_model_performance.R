# regression model performance 

library(ggplot2)
library(ggpubr)
library(ggprism)
library(ggpmisc)
library(dplyr)
library(rstatix)
getwd()
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/')

# MAE     ### first version :not used ###
# random_performace <- c(67.235,66.545,65.312,67.763,64.519)
# random_performace <- c(48.24789419471177, 48.47003134445054, 48.67191090840066, 48.37981205486819, 48.675391582117044, 48.735468159593445, 48.52746259113615, 48.69293423090039, 48.53143056009781, 48.57925514461615)
# mean(random_performace)
# sd(random_performace)

# model_ <- read.csv('tail10.csv', header = FALSE)
# model_performance <- model_$V1
#a <- c()
#for(val in model_){
#  a <- append(a, 'regression')
#}
#model_performance <- c(14.444590,16.961843,17.228097,17.073407,16.389933,15.797971,17.220899,15.820580)
#mean(model_performance)
#sd(model_performance)

# modelreg <- data.frame(models= a, mse=model_performance)
# modelreg

# modelrand <- data.frame(models= c('random','random', 'random','random', 'random'), mse=random_performace)
# modelrand
# merge data
# merge_model <- rbind(modelreg, modelrand)
# merge_model

# t检验
#df_p_val <- rstatix::t_test(merge_model, mse ~ models)%>% 
#  rstatix::add_xy_position()
#df_p_val
#p <- ggplot(merge_model, aes(x = models, y = mse)) +
#  geom_boxplot(alpha = 0.5, aes(fill = models)) +
#  geom_point(position = position_jitter(seed = 1, width = 0.2)) +
#  theme_prism() +
#  theme_classic() +
#  ylab('Mean Absolute Error (MAE)') +
#  xlab('Models') + 
#  scale_y_continuous(expand = c(0, 0), limits = c(0,80)) 

# p + add_pvalue(df_p_val, 
#               label = "p = {p}",
#               remove.bracket = TRUE)

# ggsave('regression_model_performance_ath.pdf',width = 8, height = 6,units = 'in',dpi=300)

# Distance
# library(reshape2)
# setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression model/')
# df <- read.csv('/Users/zhusitao/Downloads/TSARL_Random_model_performance.csv')
# head(df)
# df <- melt(df)
# colnames(df) <- c('models', 'distance')
# head(df)
# # geom_boxplot(aes(fill = models), colour = "black") + 
# p <- ggplot(df, aes(x = models, y = distance)) +
#   geom_boxplot(aes(fill = models), colour = "black") + 
#   theme_prism() +
#   theme_classic() +
#   ylab('Distance predicted from TSS') +
#   xlab('Models') 

# p
# # + scale_y_continuous(expand = c(0, 0), limits = c(0,80)) 
# 
# df_p_val <- rstatix::t_test(df, distance ~ models)%>% 
#   rstatix::add_xy_position()
# df_p_val
# p + add_pvalue(df_p_val, 
#                label = "p = {p}",
#                remove.bracket = TRUE)
# ggsave('regression_model_performance_distance.pdf',width = 8, height = 6,units = 'in',dpi=300)

### r_square 
# ath
# /home/zhusitao/AI/TSS_Predict/ath/regression/prediction_interval_fold0.csv
# Fig4b
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/')
r_square <- read.csv('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/ath/prediction_interval_fold0.csv')
# r_square <- read.csv('/Users/zhusitao/Downloads/prediction_interval_fold0.csv')
# r_square <- filter(r_square, label>50)
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

# TBF1
r_square <- read.csv('/Users/zhusitao/Downloads/TBF1_pred.csv')
ggplot(r_square,aes(prediction, Label)) +
  geom_point(alpha=0.6,color='black', size=0.8) +
  geom_smooth(method = "lm", se=FALSE, color="black", formula = my.formula) +
  stat_poly_eq(formula = my.formula, 
               aes(label = paste(..eq.label.., ..rr.label.., sep = "~~~"),color='red'), 
               parse = TRUE) +
  xlab("Predicted distance (nt)") +
  ylab("Observed distance (nt)") +
  theme_classic() 

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


# General Plant model 
# 总模型的训练集表现, 毕业论文中使用
# /home/zhusitao/AI/TSS_Predict/PlantModel/TBF1_regression/prediction_interval_fold0.csv

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

# Plant in other species
# 总模型在新物种中的表现 Fig4e
# setaria_predict.csv TX2783_predict.csv tx436_predict.csv
r_square <- read.csv('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/Plant/setaria_predict.csv')
r_square <- read.csv('/Users/zhusitao/Downloads/TX2783_predict.csv')
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
# + scale_x_continuous(breaks = seq(0,150,50))
ggsave('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/Plant/setaria_predict.pdf',
       width = 8, height = 6,units = 'in',dpi=300)


# Label distribution 
label <- read.csv('/Users/zhusitao/Downloads/AS.csv')

head(label)
ggplot(label, aes(x = AS5, y=AS_CDS)) + geom_point() +xlim(0,25) + ylim(0,20)
ggplot(data = label, aes(x = Label)) + geom_density() + #+xlim(0,25)
ggplot(data = label, aes(x = Label)) + geom_boxplot() 

### predict interval accuracy 
# /home/zhusitao/AI/TSS_Predict/PlantModel/another_512_regress/ensemble_test/performance.py
# /home/zhusitao/AI/TSS_Predict/PlantModel/final_version/regress/peakCount_tanh/performance.py
# dataset <- data.frame('threshold'=c(10,20,30,40,50,60,70,80,90,100),'ratio'=c(0.8032,0.884,0.9234,0.9478,0.9623,0.973,0.9802,0.9869,0.9911,0.9941))

# ath result
#dataset <- data.frame('threshold'=c(1,2,3,4,5,6,7,8,9,10,20,30),
#                      'ratio'=c(0.51,0.55,0.59,0.63,0.66,0.69,0.72,0.74,0.76,0.78, 0.89, 0.93))
# Fig4c
# version 20230220
#dataset <- data.frame('threshold'=c(1,5,10,20,30, 40, 50),
#                      'ratio'=c(0.07,0.11,0.21, 0.46, 0.65, 0.77, 0.85))
# version 20230322
# dataset <- data.frame('threshold'=c(1,5,10,20,30, 40, 50),
#                      'ratio'=c(0.07,0.14,0.26, 0.50, 0.66, 0.77, 0.85))  
# version
dataset <- data.frame('threshold'=c(1,5,10,20,30, 40, 50),
                                          'ratio'=c(0.01,0.03,0.06,0.35,0.62, 0.74, 0.83)) 
head(dataset)
ggplot(data = dataset, aes(x = threshold, y = ratio)) +
  geom_bar(stat = 'identity', fill='#4FA0CA') +
  theme_classic()

ggplot(data = dataset, aes(x = threshold, y = ratio, label=ratio)) +
  geom_line(color='#4FA0CA') + 
  geom_point(color='#EDBF6F', size=3) +
  theme_classic() +
  geom_text(hjust=0, vjust=0) +
  xlab('Threshold') +  ylab('Ratio') +
  scale_y_continuous(breaks=seq(0, 1, 0.2)) + scale_x_continuous(breaks=seq(0, 60, 10))

ggsave('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/ath/predict_interval_ratio_regression.pdf',width = 8, height = 6,units = 'in',dpi=300)

# MAE 
# /home/zhusitao/AI/TSS_Predict/work.sh MAE.csv 老版本，不在使用
# MAE = read.csv('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/general_model_performance/MAE.csv')

setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/')
# version 20230220
# /home/zhusitao/AI/TSS_Predict/ath/final_version/regress/github/data/random_select_singleton/MAE.csv
# version 20230322
# /home/zhusitao/AI/TSS_Predict/ath/final_version/regress/github/data/random_select_singleton_new/MAE.csv
# sh MAE_stat.sh 
# 20230421 /home/zhusitao/AI/TSS_Predict/ath/regression/MAE.csv 
# Fig4d
MAE <- read.csv('MAE.csv') # 4 models
head(MAE)
MAE_no_plant <- filter(MAE, Species!="plant")
ggplot(data = MAE_no_plant, aes(x=Species, y=MAE)) + 
  geom_boxplot(outlier.shape = NA) + theme_classic() +
  geom_jitter(aes(color=Species, fill=Species), size=3, 
              shape=21, alpha=0.9, width= 0.3, height = 0.3) 
  # stat_boxplot(geom='errorbar', width=0.15)
ggsave('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/MAE_20230421.pdf',width = 8, height = 6,units = 'in',dpi=300)

# Genreal model in other two species MAE
# goem_bar 
# /home/zhusitao/AI/TSS_Predict/PlantModel/final_version/regress/github/data/random_select_singleton/setaria
# python get_mae.py
# FigS7c
setwd('/Users/zhusitao/R_workspace/R_script/project/TSS_annotation/regression_model/')
df <- data.frame('Species'= c('S.viridis','S.bicolor(Tx2783)', 'S.bicolor(Tx436)'), 
                 'MAE'= c(19.85,18.97,19.44))
df
ggplot(data = df, aes(x = Species, y = MAE, fill=Species)) +
  geom_bar(width = 0.7, stat = 'identity') + theme_classic()
ggsave('new_species_MAE.pdf',width = 8, height = 6,units = 'in',dpi=300)
