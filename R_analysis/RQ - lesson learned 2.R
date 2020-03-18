# What we learned section
library(effsize)
library(distdiff)
par(mar = c(2,0.1,0.1,0.1))


# Topic 0
topic_X_counts <- read.csv("../dataset/topic_0_out_of_5_count_per_hackathon_txt_what_we_learned.csv", 
                           encoding = "UTF-8" ,
                           stringsAsFactors = FALSE,
                           na.strings=c("","NA"))
topic_X_large_hacks <- subset(topic_X_counts, popular == "Yes")
topic_X_small_hacks <- subset(topic_X_counts, popular == "No")
comp.dist.plot(topic_X_large_hacks$Topic_X_proportion,
               topic_X_small_hacks$Topic_X_proportion,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
cliff.delta(topic_X_large_hacks$Topic_X_proportion,
            topic_X_small_hacks$Topic_X_proportion)
wilcox.test(topic_X_large_hacks$Topic_X_proportion,
            topic_X_small_hacks$Topic_X_proportion,
            alternative = "greater")


# Topic 1
topic_X_counts <- read.csv("../dataset/topic_1_out_of_5_count_per_hackathon_txt_what_we_learned.csv", 
                           encoding = "UTF-8" ,
                           stringsAsFactors = FALSE,
                           na.strings=c("","NA"))
topic_X_large_hacks <- subset(topic_X_counts, popular == "Yes")
topic_X_small_hacks <- subset(topic_X_counts, popular == "No")
comp.dist.plot(topic_X_large_hacks$Topic_X_proportion,
               topic_X_small_hacks$Topic_X_proportion,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
cliff.delta(topic_X_large_hacks$Topic_X_proportion,
            topic_X_small_hacks$Topic_X_proportion)
wilcox.test(topic_X_large_hacks$Topic_X_proportion,
            topic_X_small_hacks$Topic_X_proportion,
            alternative = "greater")

num_devs <- read.csv("../Python_scripts/dorminant_5_topics_txt_what_we_learned_doc.csv", 
                     encoding = "UTF-8" ,
                     stringsAsFactors = FALSE,
                     na.strings=c("","NA"))
num_dev_large_hacks <- subset(num_devs, popular == "Yes")
num_dev_small_hacks <- subset(num_devs, popular == "No")
comp.dist.plot(num_dev_large_hacks$Num_Devs,
               num_dev_small_hacks$Num_Devs,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
cliff.delta(num_dev_large_hacks$Num_Devs,
            num_dev_small_hacks$Num_Devs)
wilcox.test(num_dev_large_hacks$Num_Devs,
            num_dev_small_hacks$Num_Devs,
            alternative = "greater")


# Topic 2
topic_X_counts <- read.csv("../dataset/topic_2_out_of_5_count_per_hackathon_txt_what_we_learned.csv", 
                           encoding = "UTF-8" ,
                           stringsAsFactors = FALSE,
                           na.strings=c("","NA"))
topic_X_large_hacks <- subset(topic_X_counts, popular == "Yes")
topic_X_small_hacks <- subset(topic_X_counts, popular == "No")
comp.dist.plot(topic_X_large_hacks$Topic_X_proportion,
               topic_X_small_hacks$Topic_X_proportion,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
cliff.delta(topic_X_large_hacks$Topic_X_proportion,
            topic_X_small_hacks$Topic_X_proportion)
wilcox.test(topic_X_large_hacks$Topic_X_proportion,
            topic_X_small_hacks$Topic_X_proportion,
            alternative = "two.sided")


# Topic 3
topic_X_counts <- read.csv("../dataset/topic_3_out_of_5_count_per_hackathon_txt_what_we_learned.csv", 
                           encoding = "UTF-8" ,
                           stringsAsFactors = FALSE,
                           na.strings=c("","NA"))
topic_X_large_hacks <- subset(topic_X_counts, popular == "Yes")
topic_X_small_hacks <- subset(topic_X_counts, popular == "No")
comp.dist.plot(topic_X_large_hacks$Topic_X_proportion,
               topic_X_small_hacks$Topic_X_proportion,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
cliff.delta(topic_X_large_hacks$Topic_X_proportion,
            topic_X_small_hacks$Topic_X_proportion)
wilcox.test(topic_X_large_hacks$Topic_X_proportion,
            topic_X_small_hacks$Topic_X_proportion,
            alternative = "greater")


# Topic 4
topic_X_counts <- read.csv("../dataset/topic_4_out_of_5_count_per_hackathon_txt_what_we_learned.csv", 
                           encoding = "UTF-8" ,
                           stringsAsFactors = FALSE,
                           na.strings=c("","NA"))
topic_X_large_hacks <- subset(topic_X_counts, popular == "Yes")
topic_X_small_hacks <- subset(topic_X_counts, popular == "No")
comp.dist.plot(topic_X_large_hacks$Topic_X_proportion,
               topic_X_small_hacks$Topic_X_proportion,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
cliff.delta(topic_X_large_hacks$Topic_X_proportion,
            topic_X_small_hacks$Topic_X_proportion)
wilcox.test(topic_X_large_hacks$Topic_X_proportion,
            topic_X_small_hacks$Topic_X_proportion,
            alternative = "greater")
