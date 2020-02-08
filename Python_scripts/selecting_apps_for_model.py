import pandas as pd
import os
import numpy as np

# df_apps = pd.read("../dataset/all_project_cleaned.csv")
df_apps = pd.read_csv("../dataset/all_project_temp.csv")
df_hackathons = pd.read_csv("../dataset/all_hackathons.csv")

# only get apps that are submitted to a hackathon
df_apps.dropna(subset=['hackathon_urls'], inplace=True)

# drop hackathons that have not ended at the moment
df_hackathons = df_hackathons[df_hackathons.is_ended == True]

# retain games t

# Get later hackathon end date




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