all_projects <- read.csv("../dataset/all_project_with_git_info.csv", 
                      encoding = "UTF-8" ,
                      stringsAsFactors = FALSE,
                      na.strings=c("","NA"))


# Dive deeper............
winning_project <- subset(all_projects, num_titles > 0)
non_winning_project <- subset(all_projects, num_titles == 0)

library(distdiff)
library(effsize)

# Description length
wilcox.test(winning_project$desc_len,
            non_winning_project$desc_len,
            alternative = "greater")
cliff.delta(winning_project$desc_len,
            non_winning_project$desc_len)

par(mar = c(2,0.1,0.1,0.1))
comp.dist.plot(log(winning_project$desc_len + 1), 
               log(non_winning_project$desc_len + 1),
               legend1 = "Won at least one title",
               legend2 = "Did not win any title",
               legendpos = "topleft",
               cut = FALSE)

# Num screenshots
wilcox.test(winning_project$num_imgs,
            non_winning_project$num_imgs,
            alternative = "greater")
cliff.delta(winning_project$num_imgs,
            non_winning_project$num_imgs)

par(mar = c(2,0.1,0.1,0.1))
comp.dist.plot(log(winning_project$num_imgs + 1), 
               log(non_winning_project$num_imgs + 1),
               legend1 = "Won at least one title",
               legend2 = "Did not win any title",
               legendpos = "topleft",
               cut = FALSE)

# Num buildwiths
wilcox.test(winning_project$num_buildWiths,
            non_winning_project$num_buildWiths,
            alternative = "greater")
cliff.delta(winning_project$num_buildWiths,
            non_winning_project$num_buildWiths)

par(mar = c(2,0.1,0.1,0.1))
comp.dist.plot(log(winning_project$num_buildWiths + 1), 
               log(non_winning_project$num_buildWiths + 1),
               legend1 = "Won at least one title",
               legend2 = "Did not win any title",
               legendpos = "topleft",
               cut = FALSE)

# Average commit per day
winning_project$average_daily_commits <- winning_project$num_commits_post_hack / winning_project$max_num_days_post_commit
non_winning_project$average_daily_commits <- non_winning_project$num_commits_post_hack / non_winning_project$max_num_days_post_commit
wilcox.test(winning_project$average_daily_commits,
            non_winning_project$average_daily_commits,
            alternative = "greater")
cliff.delta(winning_project$average_daily_commits,
            non_winning_project$average_daily_commits)
comp.dist.plot(log(winning_project$average_daily_commits + 1), 
               log(non_winning_project$average_daily_commits + 1),
               legend1 = "Won at least one title",
               legend2 = "Did not win any title",
               legendpos = "topleft",
               cut = FALSE)

par(mar = c(2,0.1,0.1,0.1))
comp.dist.plot(log(winning_project$num_buildWiths + 1), 
               log(non_winning_project$num_buildWiths + 1),
               legend1 = "Won at least one title",
               legend2 = "Did not win any title",
               legendpos = "topleft",
               cut = FALSE)




# Num commits post hack
wilcox.test(winning_project$num_commits_post_hack,
            non_winning_project$num_commits_post_hack,
            alternative = "greater")
cliff.delta(winning_project$num_commits_post_hack,
            non_winning_project$num_commits_post_hack)

par(mar = c(2,0.1,0.1,0.1))
comp.dist.plot(log10(winning_project$num_pr_post_hack + 1), 
               log10(non_winning_project$num_pr_post_hack + 1),
               legend1 = "Won at least one title",
               legend2 = "Did not win any title",
               legendpos = "topleft",
               cut = FALSE)



# Num issues post hack
wilcox.test(winning_project$num_issues_post_hack,
            non_winning_project$num_issues_post_hack,
            alternative = "greater")
cliff.delta(winning_project$num_issues_post_hack,
            non_winning_project$num_issues_post_hack)
summary(winning_project$num_issues_post_hack)
summary(non_winning_project$num_issues_post_hack)











