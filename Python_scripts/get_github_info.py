import requests
import pandas as pd
import time
import os
import json
import csv

# all_projects = pd.read_csv("../dataset/all_projects_cleaned.csv")
# all_projects = pd.read_csv("../dataset/all_project_ended_hack_with_git_repo.csv")
all_projects = pd.read_csv("./fix.csv")
# all_projects.dropna(subset=['hackathon_urls'], inplace=True)
print("{} softwares submitted to a hackathon.".format(len(all_projects)))


# drop apps do not have github/gitlab link
all_projects.dropna(subset=['software_url'], inplace=True)
all_projects = all_projects[all_projects.software_url.str.contains("github.com") | all_projects.software_url.str.contains("gitlab.com")]
print("{} softwares that provide github/gitlab links.".format(len(all_projects)))

# Take half
# x = 0
# y = len(all_projects)/2
# z = len(all_projects)
# all_projects.drop(all_projects.loc[y:z].index, inplace=True)
# all_projects.to_csv("second_half.csv", encoding='utf-8-sig', index=False)

# print(all_projects)
# exit()

unique_git_link = [git_url for git_url in all_projects['software_url'].str.split("\|\|").explode().drop_duplicates().tolist() if "github.com" in git_url or "gitlab.com" in git_url]
# print(unique_git_link)
print("{} unique github/gitlab links.".format(len(unique_git_link)))
# exit()

# input("Test")
# all_hackathons = pd.read_csv("./dataset/all_hackathons_temp.csv")
# print("{} total hackathons.".format(len(all_hackathons)))
# all_hackathons = all_hackathons[all_hackathons["is_ended"] == True]
# print("{} hackathons have ended.".format(len(all_hackathons)))

# GitHub
GH_URL = "https://api.github.com"
gh_head = {'Authorization': 'Bearer 44de7e8a01fff075e09e1714b47e57dbff17ed07',
           'Accept'       : 'application/vnd.github.v3+json'}
github_sleeptime = 0.9

# GitLab
GL_URL = "https://gitlab.com/api/v4/projects"
gl_head = {'Authorization': 'Bearer ee1PrQS7GNJaokkruo5n'}
gitlab_sleeptime = 0.3


json_res = requests.get(url = GH_URL + "/rate_limit", headers=gh_head).json()
print("Current limit: " + str(json_res['resources']['core']['remaining']))

num_inaccessible_github_repos = 0
num_inaccessible_gitlab_repos = 0
repo_groups = {}

for i, row in all_projects.iterrows():
    if pd.isna(row['software_url']):
        continue
    software_urls = row['software_url'].lower().split("||")

    for url in software_urls:
        if "github.com" in url: #NOTE GitHub rate limit is 5000 per hour (or 83 per minute)
            print("Found github link {} for project {}.".format(url, row['project_name']))
            url_comp = url.split("/")

            if len(url_comp) < 5:
                repo_groups[row['project_url']] = url
                continue

            user = url_comp[3]
            repo = url_comp[4].split("#")[0]
            print("Username: " + user + ". Github repo: " + repo)
            
            # Overall information: GH_URL + "/repos/{user}/{repo_name}"
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
            
                # query github api for commits information:  GH_URL + "/repos/{user}/{repo_name}/commits"
                print("==Querying for {}.".format(what))
                target_url = GH_URL + "/repos/{}/{}/{}".format(user, repo, what.replace("_", "/"))
                print("==Target url: {}".format(target_url))

                response = requests.get(url = target_url, headers=gh_head)

                if response.status_code == 200:
                    json_res = response.json()

                    json_file_name = "../githubdata/{}/{}_{}_{}_{}.json".format(what, user, repo, "github", what)
                    os.makedirs(os.path.dirname(json_file_name), exist_ok=True)
                    with open(json_file_name, 'w+') as outfile:
                        json.dump(json_res, outfile, indent=4)
                else:
                    num_inaccessible_github_repos += 1
                    print("Inaccessible github repo!! Error code: {}.".format(response.status_code))
            
                time.sleep(github_sleeptime)

        elif "gitlab.com" in url: #NOTE GitLab rate limit is 600 per minute
            # Sample gitlab link: https://gitlab.com/gitlab-org/gitlab
            # Issues:  https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/issues?scope=all
            # Commits: https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/repository/commits
            # Merge requests: https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/merge_requests?scope=all
            # Forks: https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/forks
            # Starrers: https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/starrers
            # Events: https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/events
            # Contributors: https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/repository/contributors
            print("Found gitlab link {} for project {}.".format(url, row['project_name']))
            url_comp = url.split("/")
            if len(url_comp) < 5:
                repo_groups[row['project_url']] = url
                continue

            user = url_comp[3]
            repo = url_comp[4]
            print("Username: " + user + ". Gitlab repo: " + repo)

            api_param = {
                "issues"       : "issues?scope=all",
                "commits"      : "repository/commits",
                "pulls"        : "merge_requests?scope=all",
                "forks"        : "forks",
                "stargazers"   : "starrers",
                "events"       : "events",
                "contributors" : "repository/contributors"
            }

            for what in api_param:
                print("==Querying for {}.".format(what))
                target_url = GL_URL + "/{}%2F{}/{}".format(user, repo, api_param[what])
                print("==Target url: {}".format(target_url))

                response = requests.get(url = target_url, headers=gl_head)
                # input("Here...")
                if response.status_code == 200:
                    json_res = response.json()

                    json_file_name = "../gitlabdata/{}/{}_{}_{}_{}.json".format(what, user, repo, "gitlab", what)
                    os.makedirs(os.path.dirname(json_file_name), exist_ok=True)
                    with open(json_file_name, 'w+') as outfile:
                        json.dump(json_res, outfile, indent=4)
                else:
                    num_inaccessible_gitlab_repos += 1
                    print("Inaccessible gitlab repo!! Error code: {}.".format(response.status_code))
            
                time.sleep(gitlab_sleeptime)

        json_res = requests.get(url = GH_URL + "/rate_limit", headers=gh_head).json()
        print("Current limit: " + str(json_res['resources']['core']['remaining']))   
        # input("Here......")     

# print("Number of inaccessible Github repos: {}.".format(num_inaccessible_github_repos))
# print("Number of inaccessible Gitlab repos: {}.".format(num_inaccessible_gitlab_repos))

# Write repo group url to file

if repo_groups:
    output = "repo_group.csv"
    header = ["project_url", "repo_group_url"]

    if os.path.exists(output):
        os.remove(output)

    with open(output, 'w', encoding='utf-8-sig', newline='') as f:  # Just use 'w' mode in 3.x
        writer = csv.DictWriter(f, fieldnames=header)

        writer.writeheader()
        for key in repo_groups:
            writer.writerow({"project_url": key, 
                            'repo_group_url': repo_groups[key]})

    f.close()