# Script description

## Cleaning data

[selecting_apps_for_model.py](selecting_apps_for_model.py): reads project metadata, computes some features, and retains only projects that have git links. These projects were submmitted to hackathons that have ended at the time of collection.

[clean_data.py](clean_data.py) : replaces some erroneous URLs for some hackathon projects.

## Retrieving and processing Github information

[get_github_info.py](get_github_info.py) : retrieves sourcecode information of the projects (in ended hackathons) that provide github/gitlab links using Github/Gitlab API

[process_git_info.py](process_git_info.py) : retrieves sourcecode information using Github/Gitlab API for projects that have git links.

## Topic modeling

[topic-modeling.ipynb](topic-modeling.ipynb) : Extracts topics using LDA technique. Produce:

Example: 
- [topic_0_out_of_5_count_per_hackathon_txt_what_we_learned.csv](../dataset/topic_0_out_of_5_count_per_hackathon_txt_what_we_learned.csv) : For topic 0 (among 5 topics of the "What we learned" section in the description), for each hackathon, show the number of projects where this topic is dominant and its contribution.
- [dominant_5_topics_txt_what_we_learned_doc.csv](../dataset/dominant_5_topics_txt_what_we_learned_doc.csv) : shows topic and topic keyword, topic contribution for each document that is extracted from the "What we learned" section.

[count_topic_per_hacks.py](count_topic_per_hacks.py) : For each hackathon, count the number of projects that have a particular topic X as the dominant topic and the proportion of that count over the total number of the hackathon.

