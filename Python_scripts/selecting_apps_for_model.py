import pandas as pd
import os
import numpy as np

# df_apps = pd.read("../dataset/all_project_cleaned.csv")
df_apps = pd.read_csv("../dataset/all_projects_cleaned.csv")
df_hackathons = pd.read_csv("../dataset/all_hackathons_cleaned.csv")

# only get apps that are submitted to a hackathon
df_apps.dropna(subset=['hackathon_urls'], inplace=True)
print("{} softwares submitted to a hackathon.".format(len(df_apps)))

# drop hackathons that have not ended at the moment
df_hackathons = df_hackathons[df_hackathons.is_ended == True]
print("{} hackathons have ended.".format(len(df_hackathons)))

# retain games whose all targeted hackathons have ended
ended_hackathon_urls = [url for url in df_hackathons['url'].tolist()]
s = df_apps['hackathon_urls'].str.split('\|+', expand=True).stack().isin(ended_hackathon_urls).groupby(level=0).all()
df_apps = df_apps[s]
print("{} softwares whose hackathons have all ended.".format(len(df_apps)))

# Get later hackathon end date
df_hackathons.set_index("url", inplace=True)
def find_max_date(hackathon_urls):
    return df_hackathons.loc[hackathon_urls.split('||'), 'latest_submission_date'].max()
df_apps["latest_hackathon_end_date"] = df_apps["hackathon_urls"].apply(find_max_date)  
print(len(df_apps))

# Calculate number of developer
df_apps["num_devs"] = df_apps["author"].map(lambda a: len(a.split("||")) if pd.notna(a) else 0)

# Calculate number of hackathons
df_apps["num_hackathons"] = df_apps["hackathon_names"].map(lambda a: len(a.split("||")) if pd.notna(a) else 0)

# Calculate number of winning titles
df_apps["num_titles"] = df_apps["win_titles"].map(lambda a: len([i for i in a.replace("<>", "||").split("||") if i]) if pd.notna(a) else 0)

# Calculate number of technology used
df_apps["num_buildWiths"] = df_apps["build_with"].map(lambda a: len(a.split("||")) if pd.notna(a) else 0)


# Write to file
output = "../dataset/all_project_ended_hack.csv"
if os.path.exists(output):
    os.remove(output)

df_apps.to_csv(output, encoding='utf-8-sig', index=False)


# drop apps do not have github/gitlab link
df_apps.dropna(subset=['software_url'], inplace=True)
df_apps = df_apps[df_apps.software_url.str.contains("github.com") | df_apps.software_url.str.contains("gitlab.com")]
print("{} softwares that provide github/gitlab links.".format(len(df_apps)))

# Write to file
output = "../dataset/all_project_ended_hack_with_git_repo.csv"
if os.path.exists(output):
    os.remove(output)

df_apps.to_csv(output, encoding='utf-8-sig', index=False)