import csv
import os
from pydriller import Repository
from tqdm import tqdm
import git
import config
import itertools
import argparse

LIMIT = None

if __name__ == "__main__":
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--limit",
        type=int,
        help="Limit how many commits are fetched",
    )
    args = argparser.parse_args()
    if args.limit:
        LIMIT = args.limit
    
    # Count commits for cool progress bar
    if os.path.isdir(config.REPO_PATH):
        repo = git.Repo(config.REPO_PATH)
        totalcommits = int(repo.git.rev_list("--count", "HEAD"))
        display_total = min(totalcommits, LIMIT) if LIMIT else totalcommits
    else:
        display_total = None

    DEVS = set()
    commits_iter = Repository(config.REPO_PATH).traverse_commits()
    if LIMIT:
        commits_iter = itertools.islice(commits_iter, LIMIT)

    for commit in tqdm(commits_iter, total=display_total, desc="Processing commits"):
        # Check that both the author and committer have emails and names
        if commit.author.name and commit.author.email:
            DEVS.add((commit.author.name, commit.author.email))
        if commit.committer.name and commit.committer.email:
            DEVS.add((commit.committer.name, commit.committer.email))

    DEVS = sorted(DEVS)

    file_path = f"project1devs/{config.TEAM_MEMBER.lower().strip()}/devs.csv"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quotechar='"')
        writer.writerow(["name", "email"])
        writer.writerows(DEVS)
