# Dataset description

## I. Hackathon datasets

[all_hackathons_raw.csv](all_hackathons_raw.csv): metadata of all hackathons at the time of collection (Total: 2,991 rows).

[all_hackathons_cleaned.csv](all_hackathons_cleaned.csv): metadata of all hackathons that have ended (total: 2,195 rows).

[all_hackathons_numsub.csv](all_hackathons_numsub.csv): number of submissions per hackathon that has ended (total: 2,195 rows).

[hackathons_top_bot_20.csv](hackathons_top_bot_20.csv): labelled popular (top 20% in number of submissions) and non-popular (bottom 20%) hackathons (total: 692 rows).


## II. Project datasets
[all_projects_raw.csv](all_projects_raw.csv): metadata of all projects at the time of crawling (total: 140,699 rows).

[all_projects_cleaned.csv](all_projects_cleaned.csv): metadata of all projects that have been submitted to a hackathon (total: 111,169 rows)


## III. Project datasets (of hackathons that ended)

### a. Metadata and text decription
    
[all_project_ended_hack.csv](all_project_ended_hack.csv): contains the metadata of all hackathons projects of the hackathons that have ended (total: 75,308 rows).

[proj_description_raw_local.csv](proj_description_raw_local.csv): the description of the hackathon projects of the hackathons that have ended (total: 75,308 rows).

### b. Github/Gitlab information

[all_project_ended_hack_with_git_repo.csv](all_project_ended_hack_with_git_repo.csv): metadata of projects that provide github/gitlab links (total: 39,471 rows).

[all_project_with_git_info.csv](all_project_with_git_info.csv): same as above but with additional information about their git repos (number of commits, number of issues, etc.) (total: 39,471 rows).


## IV. Miscellaneous

Github links that are actually a group of repositories:

[repo_group_first_half.csv](repo_group_first_half.csv)
[repo_group_2nd_half.csv](repo_group_first_half.csv)