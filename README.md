# 811372A-3007 Software Development, Maintenance and Operations 2025 Projects

This is an implementation on the example project 1, where the goal is to identify duplicate developers in a list of commiters from an open Github repository.

#### Running the analysis
Here are instructions on how to analyze duplicate developers from an open Github repository.

1. Edit the details in `config.py`. Put the URL or path to a Github repository in the `REPO_PATH` -variable, and put your name in the `TEAM_MEMBER`-variable. This creates a new folder for your csv files.
2. Run the `fetch_devs.py`-script. If you want to limit the amount of commits that are fetched (i.e. mine less than every single commit in the repository), you can run `fetch_devs.py --limit <your-limit-here>`.
3. After you run the `fetch_devs.py`-script, check that a folder named `project1devs/<your-name-here>` has been created and contains a file named `devs.csv`.
4. Run the following script `main.py --heuristic <your-choice-here> --threshold <your-choice-here>`. This script lists the duplicate developers found by the heuristic in a csv-file in the folder named `project1devs/<your-name-here>`. You can choose between the Bird et al. heuristic and the improved version by using either `bird` or `improved` with the `--heuristic` flag when running the script. You can also choose a threshold `t` by choosing (0.7 for example) `--threshold 0.7`.

After the steps above you should have a file `devs_similarity_t=<selected-threshold>_heuristic=<selected-heuristic>` in your `project1devs/<your-name-here>` -folder. This file contains all of the duplicate developers that were found.

#### Some extra scripts included in the repository
The repository also contains the script `get_test_dataset.py`. This script was used to fetch a set of 1000 developer pairs mostly with somewhat similar names or emails for the purpose of manual labeling and heuristic performance measurements. The data that was labeled by us is included in the `test_data_1000_pairs_labeled.csv` -file. To test the precision and recall of both heuristics you can run the `calculate_recall_and_precision.py` -script. The path of the csv file has to be given using the `--validation_csv`-flag, and optionally the `--threshold`-flag can be used to select a threshold `t` to use. Additionally, `csv_comparer.py` compares the .csv files of bird and improved heuristics, and creates an excel file where unique duplicate developer pairs for each heuristic are displayed, as well as the overlapping developer pairs. To run you will have to specify the relative paths of your `devs_similarity_t=<selected-threshold>_heuristic=<selected-heuristic>` .csv files in the variables `bird_path` and `improved_path`.

