
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

### Datasets

Three initial datasets can be downloaded at: https://figshare.com/s/73a5686bf6b1670092d4

They are: 
1. raw_html_text.rar -> offline html pages of hackathon projects
2. githubdata.rar, gitlabdata.rar -> source control activity data of those projects that provide public git link

### Data cleaning and analysis

Various python scripts and a notebook for LDA are in [Python_scripts](./Python_scripts).