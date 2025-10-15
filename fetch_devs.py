import csv
import os
from pydriller import Repository
from tqdm import tqdm
import git

# This block of code take the repository, fetches all the commits,
# retrieves name and email of both the author and commiter and saves the unique
# pairs to csv
# If you provide a URL, it clones the repo, fetches the commits and then deletes it,
# so for a big project better clone the repo locally and provide filesystem path

REPO_PATH = "your_path"  # Put repo path (or url) here
TEAM_MEMBER = "your_name" # Put your name here

# Count commits for cool progress bar
repo = git.Repo(REPO_PATH)
totalcommits = int(repo.git.rev_list('--count', 'HEAD'))

DEVS = set()
for commit in tqdm(Repository(REPO_PATH).traverse_commits(), total=totalcommits, desc="Processing commits"):    # wrap with tqdm because we need a cool progress bar
    DEVS.add((commit.author.name, commit.author.email))
    DEVS.add((commit.committer.name, commit.committer.email))

DEVS = sorted(DEVS)

file_path = f'project1devs/{TEAM_MEMBER}/devs.csv'
os.makedirs(os.path.dirname(file_path), exist_ok=True)
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    writer.writerow(["name", "email"])
    writer.writerows(DEVS)
