# What's next? section
library(effsize)
library(distdiff)
par(mar = c(2,0.1,0.1,0.1))


# Topic 0, 11, 17
# topic_X_counts <- read.csv("../dataset/topic_0_out_of_25_count_per_hackathon_txt_whats_next.csv",
# topic_X_counts <- read.csv("../dataset/topic_11_out_of_25_count_per_hackathon_txt_whats_next.csv",
topic_X_counts <- read.csv("../dataset/topic_17_out_of_25_count_per_hackathon_txt_whats_next.csv",
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








# Check the number of commits
proj_what_next <- read.csv("../Python_scripts/dorminant_25_topics_txt_whats_next_doc_with_hack_type.csv", 
                           encoding = "UTF-8" ,
                           stringsAsFactors = FALSE,
                           na.strings=c("","NA"))



# Comparing projects with ten commits at least
proj_git_info <- read.csv("../Python_scripts/all_project_endedHack_gitInfo_hackType.csv", 
                          encoding = "UTF-8" ,
                          stringsAsFactors = FALSE,
                          na.strings=c("","NA"))
proj_git_info$avg_daily_commit <- proj_git_info$num_commits_post_hack / proj_git_info$max_num_days_post_commit

# Compare num commits post-hacks between large-scale and small-scale hackathon
proj_git_info_large_hacks <- subset(proj_git_info, popular == "Yes" & num_commits_post_hack > 0)
proj_git_info_small_hacks <- subset(proj_git_info, popular == "No" & num_commits_post_hack > 0)
wilcox.test(proj_git_info_large_hacks$avg_daily_commit,
            proj_git_info_small_hacks$avg_daily_commit,
            alternative = "greater")
cliff.delta(proj_git_info_large_hacks$avg_daily_commit,
            proj_git_info_small_hacks$avg_daily_commit)
comp.dist.plot(proj_git_info_large_hacks$avg_daily_commit,
               proj_git_info_small_hacks$avg_daily_commit,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)
set.seed(10)
sample_proj_git_info_small_hacks <- proj_git_info_small_hacks[sample(nrow(proj_git_info_small_hacks), 81), ]

# Compare num commits post-hacks between winner and non-winner with > 10 commits
proj_git_info_winner <- subset(proj_git_info, is_winner == "True" & num_commits_post_hack > 0)
proj_git_info_non_winner <- subset(proj_git_info, is_winner == "False" & num_commits_post_hack > 0)

nrow(proj_git_info_winner) / nrow(subset(proj_git_info, is_winner == "True"))
nrow(proj_git_info_non_winner) / nrow(subset(proj_git_info, is_winner == "False"))

wilcox.test(proj_git_info_winner$avg_daily_commit,
            proj_git_info_non_winner$avg_daily_commit,
            alternative = "greater")
cliff.delta(proj_git_info_winner$avg_daily_commit,
            proj_git_info_non_winner$avg_daily_commit)
comp.dist.plot(proj_git_info_winner$avg_daily_commit,
               proj_git_info_non_winner$avg_daily_commit,
               legend1 = "Winners",
               legend2 = "Non-winners",
               legendpos = "topright",
               cut = FALSE)

# Compare num commits post-hacks between winners/non-winners 
proj_git_info_large_hacks_winners <- subset(proj_git_info, 
                                            popular == "Yes" & 
                                              is_winner == "True" & 
                                              num_commits_post_hack > 10)
proj_git_info_large_hacks_non_winners <- subset(proj_git_info, 
                                                popular == "No" & 
                                                  is_winner == "True" & 
                                                  num_commits_post_hack > 0)
wilcox.test(proj_git_info_large_hacks_winners$avg_daily_commit,
            proj_git_info_large_hacks_non_winners$avg_daily_commit,
            alternative = "greater")
cliff.delta(proj_git_info_large_hacks_winners$avg_daily_commit,
            proj_git_info_large_hacks_non_winners$avg_daily_commit)
comp.dist.plot(proj_git_info_large_hacks_winners$avg_daily_commit,
               proj_git_info_large_hacks_non_winners$avg_daily_commit,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)



# Compare num PR post-hacks between large-scale and small-scale hackathon
proj_git_info_large_hacks <- subset(proj_git_info, is_winner == "True" & num_pr_post_hack >= 0)
proj_git_info_small_hacks <- subset(proj_git_info, is_winner == "False" & num_pr_post_hack >= 0)
summary(proj_git_info_large_hacks$num_pr_post_hack)
summary(proj_git_info_small_hacks$num_pr_post_hack)
wilcox.test(proj_git_info_large_hacks$num_pr_post_hack,
            proj_git_info_small_hacks$num_pr_post_hack,
            alternative = "greater")
cliff.delta(proj_git_info_large_hacks$num_pr_post_hack,
            proj_git_info_small_hacks$num_pr_post_hack)
comp.dist.plot(proj_git_info_large_hacks$num_pr_post_hack,
               proj_git_info_small_hacks$num_pr_post_hack,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)

# Compare num PR post-hacks between winner and non-winner
proj_git_info_large_hacks <- subset(proj_git_info, is == "Yes" & num_pr_post_hack >= 0)
proj_git_info_small_hacks <- subset(proj_git_info, popular == "No" & num_pr_post_hack >= 0)
summary(proj_git_info_large_hacks$num_pr_post_hack)
summary(proj_git_info_small_hacks$num_pr_post_hack)
wilcox.test(proj_git_info_large_hacks$num_pr_post_hack,
            proj_git_info_small_hacks$num_pr_post_hack,
            alternative = "greater")
cliff.delta(proj_git_info_large_hacks$num_pr_post_hack,
            proj_git_info_small_hacks$num_pr_post_hack)
comp.dist.plot(proj_git_info_large_hacks$num_pr_post_hack,
               proj_git_info_small_hacks$num_pr_post_hack,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)



# Compare num issues post-hacks between large-scale and small-scale hackathon
proj_git_info_large_hacks <- subset(proj_git_info, is_winner == "True" & num_issues_post_hack >= 0)
proj_git_info_small_hacks <- subset(proj_git_info, is_winner == "False" & num_issues_post_hack >= 0)
summary(proj_git_info_large_hacks$num_issues_post_hack)
summary(proj_git_info_small_hacks$num_issues_post_hack)
wilcox.test(proj_git_info_large_hacks$num_issues_post_hack,
            proj_git_info_small_hacks$num_issues_post_hack,
            alternative = "greater")
cliff.delta(proj_git_info_large_hacks$num_issues_post_hack,
            proj_git_info_small_hacks$num_issues_post_hack)
comp.dist.plot(proj_git_info_large_hacks$num_issues_post_hack,
               proj_git_info_small_hacks$num_issues_post_hack,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)

# Compare num issues post-hacks between winner and non-winner
proj_git_info_large_hacks <- subset(proj_git_info, popular == "Yes" & num_issues_post_hack >= 0)
proj_git_info_small_hacks <- subset(proj_git_info, popular == "No" & num_issues_post_hack >= 0)
summary(proj_git_info_large_hacks$num_issues_post_hack)
summary(proj_git_info_small_hacks$num_issues_post_hack)
wilcox.test(proj_git_info_large_hacks$num_issues_post_hack,
            proj_git_info_small_hacks$num_issues_post_hack,
            alternative = "greater")
cliff.delta(proj_git_info_large_hacks$num_issues_post_hack,
            proj_git_info_small_hacks$num_issues_post_hack)
comp.dist.plot(proj_git_info_large_hacks$num_issues_post_hack,
               proj_git_info_small_hacks$num_issues_post_hack,
               legend1 = "Large-scale hackathons",
               legend2 = "Small-scale hackathons",
               legendpos = "topright",
               cut = FALSE)










# Function to find mode
Modes <- function(x) {
  ux <- unique(x)
  tab <- tabulate(match(x, ux))
  ux[tab == max(tab)]
}
