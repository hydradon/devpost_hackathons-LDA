all_projects$win <- as.factor(ifelse(all_projects$num_titles > 0, "Yes", "No"))
summary(all_projects$win)

# Model building
library(caret)

trControl_boot <- trainControl(classProbs = TRUE,
                               method = "boot",
                               number = 100, 
                               savePredictions = TRUE,
                               summaryFunction = twoClassSummary)

hackathon_project_model <- train(win ~ desc_len + num_imgs + num_buildWiths + num_devs,            
                                 data = all_projects,
                                 method = "glm",
                                 family = "binomial",
                                 trControl = trControl_boot)

# plot ROC
library(ggplot2)
library(plotROC)
library(scales)

# All
roc_plot <- ggplot(hackathon_project_model$pred, 
                   aes(m = Yes, d = factor(obs, levels = c("Yes", "No")))) + 
  geom_roc(labels=FALSE)
roc_plot + 
  style_roc(theme = theme_grey, ylab = "Sensitivity") +
  annotate("text", x = .75, y = .25, 
           label = paste("AUC =", round(calc_auc(roc_plot)$AUC, 2)))+
  scale_x_continuous("1 - Specificity", breaks = seq(0, 1, by = .1))
