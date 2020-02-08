import pandas as pd
import numpy as np
import os
import re

all_projects = pd.read_csv("./dataset/all_project.csv", encoding="utf-8-sig")
all_hackathons = pd.read_csv("./dataset/all_hackathons.csv", encoding="utf-8-sig")

# Remove softwares not in any hackathon
all_projects.dropna(subset=['hackathon_urls'], inplace=True)

# drop hackathons that have not ended at the moment
all_hackathons = all_hackathons[all_hackathons.is_ended == True]


# Write projects
output = "./dataset/all_project_cleaned.csv"
if os.path.exists(output):
    os.remove(output)
all_projects.to_csv(output, encoding='utf-8-sig', index=False)

# Write hackathons
output = "./dataset/all_hackathons_cleaned.csv"
if os.path.exists(output):
    os.remove(output)
all_hackathons.to_csv(output, encoding='utf-8-sig', index=False)