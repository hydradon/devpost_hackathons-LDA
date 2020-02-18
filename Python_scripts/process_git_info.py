import pandas as pd
import json
import numpy as np
import os
import csv

df_apps = pd.read_csv("../dataset/all_project_ended_hack_with_git_repo.csv")

# data = [["https://devpost.com/software/yargs", "2017-03-08T18:16:02-05:00", "http://yargs.js.org/||https://github.com/yargs/yargs"]]
# df_apps = pd.DataFrame(data, columns= ['project_url', 'latest_hackathon_end_date', 'software_url'])

error_repos = {}

for i, row in df_apps.iterrows():
    last_hack_end_date = pd.to_datetime(row["latest_hackathon_end_date"], utc = True)

    software_urls = row['software_url'].lower().split("||")
    
    github_urls = [url for url in software_urls if "github.com" in url]
    gitlab_urls = [url for url in software_urls if "gitlab.com" in url]

    num_commits_post_hack = 0  #including commits from all github and gitlab repo of the software
    max_num_days_post_commit = 0
    
    num_contributors = 0
    num_events_post_hack = 0

    num_pr_post_hack = 0
    num_pr_comments_post_hack = 0

    num_issues_post_hack = 0
    num_issues_comments_post_hack = 0
    num_issues_events_post_hack = 0

    num_stars = 0
    num_forks = 0

    # Obtaining all github info
    for url in github_urls:
        url_comp = url.split("/")
        if len(url_comp) < 5:
            continue 
        user = url_comp[3]
        repo = url_comp[4].split("#")[0]
        # print("Username: " + user + ". Github repo: " + repo)

        # what = "commit"
        for what in ['commits', 
                    'pulls', 
                    'pulls_comments',
                    'stargazers',
                    'forks', 
                    'events',
                    'contributors',
                    'issues',
                    'issues_events',
                    'issues_comments']:

            json_file_name = "../githubdata/{}/{}_{}_{}_{}.json".format(what, user, repo, "github", what)
            try:
                with open(json_file_name, 'r') as f:
                    # print("Github data found")
                    github_data = json.load(f)

                    if what == "commits":
                        for item in github_data:
                            date = pd.to_datetime(item["commit"]["author"]["date"], utc = True)
                            day_diff = (date - last_hack_end_date).total_seconds()/86400.0
                            
                            # Get maximum days between latest commit and hackathon end date
                            max_num_days_post_commit = day_diff if day_diff > max_num_days_post_commit else max_num_days_post_commit

                            # Only consider commits that are made after at least 1 day post hackathon
                            # This is to filter any commits whose purpose is just for tidying up the project.
                            # print(day_diff)
                            # print(date > last_hack_end_date)
                            if (date > last_hack_end_date) and (day_diff > 1):
                                num_commits_post_hack += 1

                    elif what == "contributors":
                        num_contributors += len(github_data)

                    elif what == "events":
                        for item in github_data:
                            date =  pd.to_datetime(item["created_at"], utc = True)
                            day_diff = (date - last_hack_end_date).total_seconds()/86400.0
                            num_events_post_hack += 1 if (date > last_hack_end_date) & (day_diff > 1) else 0
                    
                    elif what == "pulls":
                        for item in github_data:
                            date =  pd.to_datetime(item["created_at"], utc = True)
                            day_diff = (date - last_hack_end_date).total_seconds()/86400.0
                            num_pr_post_hack += 1 if (date > last_hack_end_date) & (day_diff > 1) else 0

                    elif what == "pulls_comments":
                        for item in github_data:
                            date =  pd.to_datetime(item["created_at"], utc = True)
                            # day_diff = (comment_date - last_hack_end_date).total_seconds()/86400.0
                            num_pr_comments_post_hack += 1 if (date > last_hack_end_date) else 0

                    elif what == "issues":
                        for item in github_data:
                            date =  pd.to_datetime(item["created_at"], utc = True)
                            # day_diff = (issue_date - last_hack_end_date).total_seconds()/86400.0
                            num_issues_post_hack += 1 if (date > last_hack_end_date) else 0

                    elif what == "issues_comments":
                        for item in github_data:
                            date =  pd.to_datetime(item["created_at"], utc = True)
                            # day_diff = (issue_date - last_hack_end_date).total_seconds()/86400.0
                            num_issues_comments_post_hack += 1 if (date > last_hack_end_date) else 0

                    elif what == "issues_events":
                        for item in github_data:
                            date =  pd.to_datetime(item["created_at"], utc = True)
                            day_diff = (date - last_hack_end_date).total_seconds()/86400.0

                            num_issues_events_post_hack += 1 if (date > last_hack_end_date) & (day_diff > 1) else 0

                    elif what == "forks":
                        num_forks += len(github_data)
                    
                    elif what == "stargazers":
                        num_stars += len(github_data)

            except IOError:
                print("Github data not available")

            except Exception:
                if row['project_url'] not in error_repos:
                    error_repos[row['project_url']] = url
                else:
                    error_repos[row['project_url']] = error_repos[row['project_url']] + "||" + url

    # Obtaining all gitlab info
    for url in gitlab_urls:
        url_comp = url.split("/")
        if len(url_comp) < 5:
            continue 
        user = url_comp[3]
        repo = url_comp[4]
        # print("Username: " + user + ". Gitlab repo: " + repo)

        if len(url_comp) < 5:
            # repo_groups[row['project_url']] = url
            continue

        # what = "commit"
        for what in ['commits', 
                    'pulls', 
                    'stargazers',
                    'forks', 
                    'events',
                    'contributors',
                    'issues']:

            json_file_name = "../gitlabdata/{}/{}_{}_{}_{}.json".format(what, user, repo, "gitlab", what)
            try:
                with open(json_file_name, 'r') as f:
                    # print("Gitlab data found")
                    gitlab_data = json.load(f)

                    if what == "commit":
                        for item in gitlab_data:
                            date = pd.to_datetime(item["commit"]["author"]["date"], utc = True)
                            day_diff = (date - last_hack_end_date).total_seconds()/86400.0
                            
                            # Get maximum days between latest commit and hackathon end date
                            max_num_days_post_commit = day_diff if day_diff > max_num_days_post_commit else max_num_days_post_commit

                            # Only consider commits that are made after at least 1 day post hackathon
                            # This is to filter any commits whose purpose is just for tidying up the project.
                            num_commits_post_hack += 1 if (date > last_hack_end_date) & (day_diff > 1) else 0

                    elif what == "contributors":
                        num_contributors += len(gitlab_data)

                    elif what == "events":
                        for item in gitlab_data:
                            date =  pd.to_datetime(item["created_at"], utc = True)
                            day_diff = (date - last_hack_end_date).total_seconds()/86400.0
                            num_events_post_hack += 1 if (date > last_hack_end_date) & (day_diff > 1) else 0
                    
                    elif what == "pulls":
                        for item in gitlab_data:
                            date =  pd.to_datetime(item["created_at"], utc = True)
                            day_diff = (date - last_hack_end_date).total_seconds()/86400.0
                            num_pr_post_hack += 1 if (date > last_hack_end_date) & (day_diff > 1) else 0

                    elif what == "issues":
                        for item in gitlab_data:
                            date =  pd.to_datetime(item["created_at"], utc = True)
                            num_issues_post_hack += 1 if (date > last_hack_end_date) else 0

                    elif what == "forks":
                        num_forks += len(gitlab_data)
                    
                    elif what == "stargazers":
                        num_stars += len(gitlab_data)

            except IOError:
                print("Gitlab data not available")

            except Exception:
                if row['project_url'] not in error_repos:
                    error_repos[row['project_url']] = url
                else:
                    error_repos[row['project_url']] = error_repos[row['project_url']] + "||" + url


    # Creating new fields for the row
    df_apps.loc[i, "num_commits_post_hack"]         = num_commits_post_hack
    df_apps.loc[i, "max_num_days_post_commit"]      = max_num_days_post_commit
    df_apps.loc[i, "num_contributors"]              = num_contributors
    df_apps.loc[i, "num_events_post_hack"]          = num_events_post_hack
    df_apps.loc[i, "num_pr_post_hack"]              = num_pr_post_hack
    df_apps.loc[i, "num_pr_comments_post_hack"]     = num_pr_comments_post_hack
    df_apps.loc[i, "num_issues_post_hack"]          = num_issues_post_hack
    df_apps.loc[i, "num_issues_comments_post_hack"] = num_issues_comments_post_hack
    df_apps.loc[i, "num_issues_events_post_hack"]   = num_issues_events_post_hack
    df_apps.loc[i, "num_forks"]                     = num_forks
    df_apps.loc[i, "num_stars"]                     = num_stars
    

# Write to file
output = "../dataset/all_project_with_git_info.csv"
if os.path.exists(output):
    os.remove(output)

df_apps.to_csv(output, encoding='utf-8-sig', index=False)


# Write repo group url to file
if error_repos:
    output = "error_repo.csv"
    header = ["project_url", "error_repo_url"]

    if os.path.exists(output):
        os.remove(output)

    with open(output, 'w', encoding='utf-8-sig', newline='') as f:  # Just use 'w' mode in 3.x
        writer = csv.DictWriter(f, fieldnames=header)

        writer.writeheader()
        for key in error_repos:
            writer.writerow({"project_url": key, 
                            'error_repo_url': error_repos[key]})

    f.close()