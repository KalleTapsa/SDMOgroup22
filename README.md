# 811372A-3007 Software Development, Maintenance and Operations 2025 Projects

This is an implementation on the example project 1, where the goal is to identify duplicate developers in a list of commiters from an open Github repository.

Here are instructions on how to analyze duplicate developers from an open Github repository.

1. Edit your details to `config.py`. Use your wanted Github repository in the `REPO_PATH` -variable, and put your name in the `TEAM_MEMBER`-variable.
2. Run the `fetch_devs.py`-script. If you want to limit the amount of commits that are fetched (i.e. get less developers to `devs.csv`), you can run `fetch_devs.py --limit <your-limit-here>`.
3. After you run the `fetch_devs.py`-script, check that a folder named `project1devs/<your-name-here>` is created and there is a file named `devs.csv`.
4. Run the following script `main.py --heuristic <your-choice-here> --threshold <your-choice-here>`. This script lists the duplicate developers to a csv-file in the folder named `project1devs/<your-name-here>`. You can choose between the Bird et al. heuristic and the improved version by using either `bird` or `improved` -flag when running the script. You can also choose your threshold `t` by choosing (0.7 for example) `--threshold 0.7`.


After doing the steps above you should have a file `devs_similarity_t=<selected-threshold>` in your `project1devs/<your-name-here>` -folder. 


