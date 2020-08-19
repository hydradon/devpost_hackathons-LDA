
### Description

In this project, I analyze the text description written by hackathon participants.

First, I crawled for data from Devpost for the metadata of all hackathon projects.

Then, for each project, I used latent Dirichlet Allocation (LDA) to automatically extract the topics from what are written. Each project page is structured as follows:

* Inspiration
* What it does
* How we built it (or How I built it)
* Challenges
* Accomplishment
* What we learned
* What's next

I applied topic modeling on each of the above sections to find out the main topics mentioned.

### The spiders

1. [devpost](./devpost): visits all projects at devpost/software/trending and crawls for all metadata. Output: [all_projects_raw.csv](./dataset/all_projects_raw.csv)

2. [devpost_hackathon](./devpost_hackathon): visits all hackathon pages extracted from the metadata of the projects and crawls for hackathon metadata. Output: [all_hackathons_raw.csv](./dataset/all_hackathons_raw.csv)

3. [devpost_app_page](./devpost_app_page): visits all project pages and saves their HTMLs. Output is stored on figshare: https://figshare.com/s/73a5686bf6b1670092d4

4. [dev_proj_desc_local](./dev_proj_desc_local): crawls the offline HTML pages (obtained above) and parses the text description into 7 sections as described in the previous part. Output: [proj_description_raw_local.csv](./dataset/proj_description_raw_local.csv)

5. [devpost_hack_num_submission](./devpost_hack_num_submission): crawls the hackathon pages and retrieves the number of submissions. Output: [all_hackathons_numsub.csv](./dataset/all_hackathons_numsub.csv) 




### Datasets

Three initial datasets can be downloaded at: https://figshare.com/s/73a5686bf6b1670092d4

They are: 
1. raw_html_text.rar -> offline html pages of hackathon projects
2. githubdata.rar, gitlabdata.rar -> source control activity data of those projects that provide public git link

### Data cleaning and analysis

Various python scripts and a notebook for LDA are in [Python_scripts](./Python_scripts).