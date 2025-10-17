import csv
import os
from pydriller import Repository
from tqdm import tqdm
import git
from config import *
import itertools
import shutil

# This block of code take the repository, fetches all the commits,
# retrieves name and email of both the author and commiter and saves the unique
# pairs to csv
# If you provide a URL, it clones the repo, fetches the commits and then deletes it,
# so for a big project better clone the repo locally and provide filesystem path

LIMIT = 5000  # Limit how many commits are fetched

# Count commits for cool progress bar
if os.path.isdir(REPO_PATH):
    repo = git.Repo(REPO_PATH)
    totalcommits = int(repo.git.rev_list('--count', 'HEAD'))
    display_total = min(totalcommits, LIMIT) if LIMIT else totalcommits
else:
    display_total = None

DEVS = set()
commits_iter = Repository(REPO_PATH).traverse_commits()
if LIMIT:
    commits_iter = itertools.islice(commits_iter, LIMIT)

for commit in tqdm(commits_iter, total=display_total, desc="Processing commits"):
    # Check that both the author and committer have emails and names
    if commit.author.name and commit.author.email:
        DEVS.add((commit.author.name, commit.author.email))
    if commit.committer.name and commit.committer.email:
        DEVS.add((commit.committer.name, commit.committer.email))

DEVS = sorted(DEVS)

file_path = f'project1devs/{TEAM_MEMBER.lower().strip()}/devs.csv'
os.makedirs(os.path.dirname(file_path), exist_ok=True)
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    writer.writerow(["name", "email"])
    writer.writerows(DEVS)
