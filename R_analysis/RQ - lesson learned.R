# What we learned section
library(effsize)
library(distdiff)


# Topic 0
topic_X_counts <- read.csv("../dataset/topic_0_count_per_hackathon_txt_what_we_learned.csv", 
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


# Topic 5 - Data handling lesson
topic_X_counts <- read.csv("../dataset/topic_5_count_per_hackathon_txt_what_we_learned.csv", 
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


# Topic 18 - Data handling lesson
topic_X_counts <- read.csv("../dataset/topic_18_count_per_hackathon_txt_what_we_learned.csv", 
                           encoding = "UTF-8" ,
                           stringsAsFactors = FALSE,
                           na.strings=c("","NA"))
topic_X_large_hacks <- subset(topic_X_counts, popular == "Yes")
topic_X_small_hacks <- subset(topic_X_counts, popular == "No")
comp.dist.plot(log(topic_X_large_hacks$Topic_X_proportion + 1),
               log(topic_X_small_hacks$Topic_X_proportion + 1),
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
cliff.delta(topic_X_large_hacks$Topic_X_proportion,
            topic_X_small_hacks$Topic_X_proportion)
wilcox.test(topic_X_large_hacks$Topic_X_proportion,
            topic_X_small_hacks$Topic_X_proportion,
            alternative = "greater")





