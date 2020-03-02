import pandas as pd
import numpy as np
import re
import os
from pprint import pprint

from gensim.models.wrappers import LdaMallet
import nltk
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt

# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

df_apps = pd.read_csv("../dataset/proj_description_raw_local.csv")
df_apps.project_url[df_apps.project_url == "D:\Research\hackathon-devpost/raw_html_text\\aux1.html"] = "D:\Research\hackathon-devpost/raw_html_text\\aux.html"


df_apps["app"] = df_apps["project_url"].map(lambda x: x.split("\\")[3].split(".")[0])



# Retrieve Hackathon
df_proj_details = pd.read_csv("../dataset/all_project_ended_hack.csv")
df_proj_details["app"] = df_proj_details["project_url"].map(lambda x: x.split("/")[4])
df_proj_hackathon_pair = df_proj_details[["app", "hackathon_urls"]]
# match hackthon with project description
txt_desc_hackathon_pair = df_apps.merge(df_proj_hackathon_pair, left_on="app", right_on="app")


text_map = [
        "txt_inspiration",
        "txt_what_it_does",
        "txt_how_we_built", # How we built it, How I built it
        "txt_challenges",
        "txt_accomplishment",
        "txt_what_we_learned",
        "txt_whats_next"]

section = text_map[6]
num_topic = 25

# Remove rows with no data
txt_desc_hackathon_pair.dropna(subset=[section], inplace=True)

# Remove punctuation
txt_desc_hackathon_pair['txt_processed'] = txt_desc_hackathon_pair[section].map(lambda x: re.sub('[,\.!?]', '', x))

# Remove rows with no data again!
txt_desc_hackathon_pair.dropna(subset=[section], inplace=True)

# Convert to lower case
txt_desc_hackathon_pair['txt_processed'] = txt_desc_hackathon_pair['txt_processed'].map(lambda x: x.lower())

# Convert to list
data = txt_desc_hackathon_pair["txt_processed"].tolist()

# Extract hackathon list
# hackathons = txt_desc_hackathon_pair["hackathon_urls"]

# Testing, only extract a few data points
# data = data[0:25]

# Remove Emails
# data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
txt_desc_hackathon_pair["txt_processed"] = txt_desc_hackathon_pair["txt_processed"].map(lambda x: re.sub('\S*@\S*\s?', '', x))

# Remove new line characters
# data = [re.sub('\s+', ' ', sent) for sent in data]
txt_desc_hackathon_pair["txt_processed"] = txt_desc_hackathon_pair["txt_processed"].map(lambda x: re.sub('\s+', ' ', x))

# Remove distracting single quotes
# data = [re.sub("\'", "", sent) for sent in data]
txt_desc_hackathon_pair["txt_processed"] = txt_desc_hackathon_pair["txt_processed"].map(lambda x: re.sub("\'", "", x))


# Remove empty description
txt_desc_hackathon_pair = txt_desc_hackathon_pair[txt_desc_hackathon_pair.txt_processed != ""]
txt_desc_hackathon_pair = txt_desc_hackathon_pair[txt_desc_hackathon_pair.txt_processed != " "]

# Convert to list
data = txt_desc_hackathon_pair["txt_processed"].tolist()

# Extract processed text - hackathon pairs
processed_txt_hackathon_pair = txt_desc_hackathon_pair[["txt_processed", "project_url", "hackathon_urls"]]
# processed_txt_hackathon_pair["project_url"] = processed_txt_hackathon_pair["project_url"].str.replace("D:\\Research\\hackathon-devpost/raw_html_text\\", "https://devpost.com/software/")
processed_txt_hackathon_pair["project_url"] = processed_txt_hackathon_pair["project_url"].map(lambda x: "https://devpost.com/software/" + x.split("\\")[3].replace(".html", ""))


# Tokenize
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

data_words = list(sent_to_words(data))
# print(data_words[1])

# Build the bigram and trigram models
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

# See trigram example
# print(trigram_mod[bigram_mod[data_words[1]]])

# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

# Remove Stop Words
data_words_nostops = remove_stopwords(data_words)

# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)

# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
nlp = spacy.load('en', disable=['parser', 'ner'])

# Do lemmatization keeping only noun, adj, vb, adv
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

# print(data_lemmatized[:1])

# Create Dictionary
id2word = corpora.Dictionary(data_lemmatized)

# Create Corpus
texts = data_lemmatized

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# Build Mallet LDA model
from gensim.models.wrappers import LdaMallet
os.environ['MALLET_HOME'] = 'D:\Research\hackathon-devpost\Python_scripts\mallet-2.0.8'
mallet_path = 'D:\Research\hackathon-devpost\Python_scripts\mallet-2.0.8\\bin\mallet' # update this path
ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, 
                                            corpus=corpus, 
                                            num_topics=num_topic, 
                                            iterations=500, # default = 1000
                                            id2word=id2word,
                                            random_seed=5) 

# Show Topics
# pprint(ldamallet.show_topics(formatted=False))

# Compute Coherence Score NOTE not working!
# coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
# coherence_ldamallet = coherence_model_ldamallet.get_coherence()
# print('\nCoherence Score: ', coherence_ldamallet)

###  Finding the dominant topic in each sentence
def format_topics_sentences(ldamodel, corpus, texts, project_url, hackathons):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]): # length of data
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents, pd.Series(project_url), pd.Series(hackathons)], axis=1)
    return(sent_topics_df)


df_topic_sents_keywords = format_topics_sentences(ldamodel=ldamallet, 
                                                  corpus=corpus, 
                                                  texts=data, 
                                                  project_url=processed_txt_hackathon_pair["project_url"].tolist(),
                                                  hackathons=processed_txt_hackathon_pair["hackathon_urls"].tolist())

# df_topic_sents_keywords.dropna(subset = ["Perc_Contribution"], inplace=True)

# Format
df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text', "Project_Url", "Hackathon_Url"]

# Format the contribution to 4 decimal places
df_dominant_topic["Topic_Perc_Contrib"] = df_dominant_topic["Topic_Perc_Contrib"].map('{:,.4f}'.format)

# Save before splitting hackathons
df_dominant_topic_sorted = df_dominant_topic.sort_values(["Dominant_Topic", "Topic_Perc_Contrib"], ascending=[True, False])
output = "./dorminant_" + str(num_topic) + "_topics_" + section + "_doc.csv"
if os.path.exists(output):
    os.remove(output)
df_dominant_topic_sorted.to_csv(output, encoding='utf-8-sig', index=False)


# Show
# print(df_dominant_topic.head(10))



# TODO split hackathon strings xyz||abc to 2 rows
# df_dominant_topic
df_dominant_topic["Hackathon_Url"] = df_dominant_topic["Hackathon_Url"].map(lambda a: a.split("||"))
df_dominant_topic = df_dominant_topic.explode("Hackathon_Url")


# temp = df_dominant_topic.merge(processed_txt_hackathon_pair, left_on="Text", right_on="txt_processed")
# temp.drop(columns = ["Topic_Perc_Contrib", "Text", "txt_processed"], inplace=True)
temp = df_dominant_topic.drop(columns = ["Document_No", "Text", "Topic_Perc_Contrib", "Keywords", "Project_Url"])
temp.drop_duplicates(inplace=True)
# input("Here")

# Find the counts of dorminant topics across hackathon
topic_hackathons_count = temp["Dominant_Topic"].value_counts()
topic_hackathons_count = topic_hackathons_count.to_frame()
topic_hackathons_count = pd.DataFrame({'Topic_Num': topic_hackathons_count.index, 
                                       'Hackathon_Count': topic_hackathons_count.Dominant_Topic})


# Write to file
output = "./dorminant_" + str(num_topic) + "_topics_" + section + "_hackathons_count.csv"
if os.path.exists(output):
    os.remove(output)
topic_hackathons_count.to_csv(output, encoding='utf-8-sig', index=False)

# ### Find the most representative document for each topic
# # Group top 5 sentences under each topic
sent_topics_sorteddf_mallet = pd.DataFrame()
sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')
for i, grp in sent_topics_outdf_grpd:
    sent_topics_sorteddf_mallet = pd.concat([sent_topics_sorteddf_mallet, 
                                             grp.sort_values(['Perc_Contribution'], ascending=[0]).head(1)], 
                                            axis=0)
# # Reset Index    
sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)
# # Format
sent_topics_sorteddf_mallet.columns = ['Topic_Num', "Topic_Perc_Contrib", "Keywords", "Text", "Project_Url", "Hackathon_Urls"]
# Show
sent_topics_sorteddf_mallet.head()

# Write to file
output = "./dorminant_" + str(num_topic) + "_topics_" + section + "_representative_text.csv"
if os.path.exists(output):
    os.remove(output)

sent_topics_sorteddf_mallet.to_csv(output, encoding='utf-8-sig', index=False)


### Topic distribution across documents
# Number of Documents for Each Topic
topic_counts = df_topic_sents_keywords['Dominant_Topic'].value_counts()
# print(topic_counts)
topic_counts_df = topic_counts.to_frame()
topic_counts_df = pd.DataFrame({'Topic_Num': topic_counts_df.index, 
                                'Project_Count': topic_counts_df.Dominant_Topic})
# input("here")

# Percentage of Documents for Each Topic
topic_contribution = round(topic_counts/topic_counts.sum(), 4)
# print(topic_contribution)
topic_contribution_df = topic_contribution.to_frame()
topic_contribution_df = pd.DataFrame({'Topic_Num': topic_contribution_df.index, 
                                      'Topic_Contrib': topic_contribution_df.Dominant_Topic})
# input("here")
# Format the contribution to 4 decimal places
topic_contribution_df["Topic_Contrib"] = topic_contribution_df["Topic_Contrib"].map('{:,.4f}'.format)

# Topic Number and Keywords
topic_num_keywords = df_topic_sents_keywords[['Dominant_Topic', 'Topic_Keywords']]

merge = topic_counts_df.merge(topic_num_keywords.rename(columns={"Dominant_Topic":"Topic_Num"}), left_index=True, right_on="Topic_Num").drop_duplicates()
final = merge.merge(topic_contribution_df, left_on="Topic_Num", right_index=True)
final_final = final.merge(topic_hackathons_count, left_on="Topic_Num", right_index=True)

# Calculate percentage of hackathons that this topic was dominant
final_final["Perc_Hackathon"] = final_final["Hackathon_Count"] / 2195.0
final_final["Perc_Hackathon"] = final_final["Perc_Hackathon"].map('{:,.2f}'.format)

final_final.drop(columns = ["Topic_Num_x", "Topic_Num_y"], inplace=True)
# final_final.Topic_Contrib = final_final.Topic_Contrib.astype(float).round(4)
# final_final = final

# Write to file
output = "./dorminant_" + str(num_topic) + "_topics_" + section + ".csv"
if os.path.exists(output):
    os.remove(output)

final_final.to_csv(output, encoding='utf-8-sig', index=False)