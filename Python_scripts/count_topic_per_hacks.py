import pandas as pd
import os

# dorminant_25_topics_txt_whats_next_doc
section = "txt_whats_next"
num_topic = 25

docs = pd.read_csv("../dataset/dorminant_" + str(num_topic) + "_topics_" + section + "_doc.csv", encoding="utf-8-sig")
topic = 15 #0, 10, 6, 9, 5

# get only topic 0
# topic_x_docs = docs[docs["Dominant_Topic"] == topic]
topic_x_docs = docs

# Split into large scale and small scale hackathon
topic_x_docs_large_hacks = topic_x_docs[topic_x_docs["popular"] == "Yes"]
topic_x_docs_small_hacks = topic_x_docs[topic_x_docs["popular"] == "No"]

# Extract number of submission
large_hacks_num_sub = topic_x_docs_large_hacks[["Hackathon_Url", "num_submission", "popular"]].drop_duplicates()
small_hacks_num_sub = topic_x_docs_small_hacks[["Hackathon_Url", "num_submission", "popular"]].drop_duplicates()

# Count number of projects with topic X in each hackathons
topic_x_count_large_hacks = topic_x_docs_large_hacks.set_index('Hackathon_Url').Dominant_Topic.eq(topic).sum(level=0).astype(int).reset_index()
topic_x_count_small_hacks = topic_x_docs_small_hacks.set_index('Hackathon_Url').Dominant_Topic.eq(topic).sum(level=0).astype(int).reset_index()

# Rename count column
topic_x_count_large_hacks.rename(columns = {"Dominant_Topic" : "Topic_X_count"}, inplace=True)
topic_x_count_small_hacks.rename(columns = {"Dominant_Topic" : "Topic_X_count"}, inplace=True)

# Merging counts with number of submission
large = topic_x_count_large_hacks.merge(large_hacks_num_sub, on="Hackathon_Url")
small = topic_x_count_small_hacks.merge(small_hacks_num_sub, on="Hackathon_Url")

# Calculate percentage of topic 0 of each hackathons
final = pd.concat([large, small])
final["Topic_X_proportion"] = final['Topic_X_count']/final['num_submission']
final["Topic_X_proportion"] = final["Topic_X_proportion"].map('{:,.4f}'.format)

# Save to file
output = "../dataset/topic_" + str(topic) + "_out_of_" + str(num_topic) + "_count_per_hackathon_" + section + ".csv"
if os.path.exists(output):
    os.remove(output)
final.to_csv(output, encoding='utf-8-sig', index=False)
