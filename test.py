import pandas as pd
import os
import json
import iso8601

user = "frichetten"
repo = "frichetten.github.io"

what = "commits"
json_file_name = "./githubdata/{}/{}_{}_{}_{}.json".format(what, user, repo, "github", what)

try:
    with open(json_file_name, 'r') as f:
        print("Github data found")
        github_data = json.load(f)

        print(len(github_data))

        for commit in github_data:
            commit_date_string = commit["commit"]["author"]["date"]
            print("Commit date: " + commit_date_string)
            commit_date = iso8601.parse_date(commit_date_string)
            # print(commit_date)

except IOError:
    print("Github data not available")

