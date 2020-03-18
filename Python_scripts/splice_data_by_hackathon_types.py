import pandas as pd
import os
import math
from natsort import index_natsorted, order_by_index


# Reading github info

num_topic = 25
section = 1
text_map = [
        # "txt_inspiration",
        # "txt_what_it_does",
        # "txt_how_we_built", # How we built it, How I built it
        "txt_challenges",
        # "txt_accomplishment",
        # "txt_what_we_learned",
        "txt_whats_next"]


topic_file_name = "dorminant_" + str(num_topic) + "_topics_" + text_map[section] + "_doc.csv"
# Read the topic vs document csv file
topic_doc = pd.read_csv("../Python_scripts/" + topic_file_name, encoding="utf-8-sig")

# Read hackathon type file
hackathons = pd.read_csv("../dataset/hackathons_top_bot_20.csv", encoding="utf-8-sig")

# # Get top and bottom 20% jam by number of submissions
# top_n = math.ceil(len(hackathons)*(20/100))
# hackathons = hackathons.reindex(index=order_by_index(hackathons.index,
#                                 index_natsorted(hackathons['num_submission'],
#                                 reverse=True)))
# top_20_hackathons = hackathons.head(top_n)
# top_20_hackathons.insert(len(top_20_hackathons.columns), 
#                     'popular',
#                     pd.Series("Yes", index=top_20_hackathons.index))
# bottom_20_hackathons = hackathons.tail(top_n)
# bottom_20_hackathons.insert(len(bottom_20_hackathons.columns), 
#                         'popular',
#                         pd.Series("No", index=bottom_20_hackathons.index))
# Combine
# final_hackathons = pd.concat([top_20_hackathons, bottom_20_hackathons])

hackathon_type = {}
for i, row in hackathons.iterrows():
    hackathon_type[row["hackathon_url"]] = row["popular"]


# Explode rows where project is submitted to multiple hackathons
# Calculate number of hackathons
topic_doc["num_hackathons"] = topic_doc["Hackathon_Url"].map(lambda a: len(a.split("||")) if pd.notna(a) else 0)
topic_doc["Hackathon_Url"] = topic_doc["Hackathon_Url"].map(lambda a: a.split("||"))
topic_doc = topic_doc.explode("Hackathon_Url")

for i, row in topic_doc.iterrows():
    topic_doc.loc[i, 'hackathon_type'] = hackathon_type.get(row["Hackathon_Url"], "None")


# Combined with git info:
project_git_info = pd.read_csv("../dataset/all_project_with_git_info.csv", encoding="utf-8-sig")
project_git_info.drop(columns = ["build_with", "desc_len", "author", "win_titles", "is_winner", "summary_len", "project_name",
                                "author_url", "num_likes", "num_imgs", "num_cmts", "start_date", "latest_hackathon_end_date",
                                "hackathon_names"], 
                      inplace=True)

temp = topic_doc.merge(project_git_info, left_on="Project_Url", right_on="project_url", how="left")           
temp.drop(columns = ["project_url", "hackathon_urls"], inplace=True)

# Write to file
output = "dorminant_" + str(num_topic) + "_topics_" + text_map[section] + "_doc_with_hack_type.csv"

if os.path.exists(output):
    os.remove(output)
temp.to_csv(output, encoding='utf-8-sig', index=False)