## Challenge section

# Comparing the proportion of the projects that face a specific challenge between large scale and small scale hackathon
library(effsize)
library(distdiff)

par(mar = c(2,0.1,0.1,0.1))
# Topic 0
topic_0_counts <- read.csv("../dataset/topic_0_count_per_hackathon_txt_challenges.csv", 
                      encoding = "UTF-8" ,
                      stringsAsFactors = FALSE,
                      na.strings=c("","NA"))
topic_0_large_hacks <- subset(topic_0_counts, popular == "Yes")
topic_0_small_hacks <- subset(topic_0_counts, popular == "No")
comp.dist.plot(topic_0_large_hacks$Topic_X_proportion,
               topic_0_small_hacks$Topic_X_proportion,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
cliff.delta(topic_0_large_hacks$Topic_X_proportion,
            topic_0_small_hacks$Topic_X_proportion)
wilcox.test(topic_0_large_hacks$Topic_X_proportion,
            topic_0_small_hacks$Topic_X_proportion,
            alternative = "greater")


# Topic 10
topic_10_counts <- read.csv("../dataset/topic_10_count_per_hackathon_txt_challenges.csv", 
                           encoding = "UTF-8" ,
                           stringsAsFactors = FALSE,
                           na.strings=c("","NA"))
topic_10_large_hacks <- subset(topic_10_counts, popular == "Yes")
topic_10_small_hacks <- subset(topic_10_counts, popular == "No")
comp.dist.plot(topic_10_large_hacks$Topic_X_proportion,
               topic_10_small_hacks$Topic_X_proportion,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
cliff.delta(topic_10_large_hacks$Topic_X_proportion,
            topic_10_small_hacks$Topic_X_proportion)


# Topic 5
topic_5_counts <- read.csv("../dataset/topic_5_count_per_hackathon_txt_challenges.csv", 
                            encoding = "UTF-8" ,
                            stringsAsFactors = FALSE,
                            na.strings=c("","NA"))
topic_5_large_hacks <- subset(topic_5_counts, popular == "Yes")
topic_5_small_hacks <- subset(topic_5_counts, popular == "No")
comp.dist.plot(topic_5_large_hacks$Topic_X_proportion,
               topic_5_small_hacks$Topic_X_proportion,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
cliff.delta(topic_5_large_hacks$Topic_X_proportion,
            topic_5_small_hacks$Topic_X_proportion)


# Topic 9
topic_9_counts <- read.csv("../dataset/topic_9_count_per_hackathon_txt_challenges.csv", 
                           encoding = "UTF-8" ,
                           stringsAsFactors = FALSE,
                           na.strings=c("","NA"))
topic_9_large_hacks <- subset(topic_9_counts, popular == "Yes")
topic_9_small_hacks <- subset(topic_9_counts, popular == "No")
comp.dist.plot(topic_9_large_hacks$Topic_X_proportion,
               # topic_5_large_hacks$Topic_X_proportion,
               topic_9_small_hacks$Topic_X_proportion,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
cliff.delta(topic_9_large_hacks$Topic_X_proportion,
            topic_9_small_hacks$Topic_X_proportion)



# Topic 6
topic_6_counts <- read.csv("../dataset/topic_6_count_per_hackathon_txt_challenges.csv", 
                           encoding = "UTF-8" ,
                           stringsAsFactors = FALSE,
                           na.strings=c("","NA"))
topic_6_large_hacks <- subset(topic_6_counts, popular == "Yes")
topic_6_small_hacks <- subset(topic_6_counts, popular == "No")
comp.dist.plot(topic_6_large_hacks$Topic_X_proportion,
               topic_6_small_hacks$Topic_X_proportion,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
cliff.delta(topic_6_large_hacks$Topic_X_proportion,
            topic_6_small_hacks$Topic_X_proportion)
wilcox.test(topic_6_large_hacks$Topic_X_proportion,
            topic_6_small_hacks$Topic_X_proportion,
            alternative = "greater")

