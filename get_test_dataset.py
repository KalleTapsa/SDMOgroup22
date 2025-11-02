import csv
import os
import sys
from tqdm import tqdm
import config
from itertools import combinations
from utils import is_potential_duplicate
import argparse
import numpy as np

def biased_sample(pairs, n_samples):
    """Sample developer pairs with bias towards potential duplicates.
    Args:
        pairs (list): List of tuples containing developer pairs
        n_samples (int): Number of samples to take
    Returns:
        list: Sampled developer pairs
    """
    sims = np.array([is_potential_duplicate(dev1, dev2) for dev1, dev2 in pairs])
    probs = sims + 0.001  # Add small number so low sims still have a chance
    probs /= probs.sum()  # Normalize to sum to 1 for np.random.choice

    # Randomly sample indices with the probabilities
    chosen_idx = np.random.choice(len(pairs), size=n_samples, replace=False, p=probs)
    return [pairs[i] for i in chosen_idx]

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Get dataset for testing heuristics."
    )
    argparser.add_argument(
        "--num_pairs",
        type=int,
        default=1000,
        required=False,
        help="Number of developer pairs to output (default: 1000)",
    )
    
    args = argparser.parse_args()
    num_pairs = args.num_pairs

    csv_file_path = os.path.join("project1devs", config.TEAM_MEMBER.lower().strip())
    raw_path = os.path.join(csv_file_path, f"test_data_{num_pairs}_pairs.csv")

    if not os.path.isfile(raw_path):
        devs_file_path = os.path.join(csv_file_path, "devs_validation.csv")
        if not os.path.isfile(devs_file_path):
            print(
                f"No csv file found at {devs_file_path}! First use fetch_devs.py to generate it."
            )
            sys.exit()

        DEVS = []
        # Read csv file with name,dev columns
        with open(devs_file_path, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                DEVS.append(row)
        # First element is header, skip
        DEVS = DEVS[1:]

        # Total combinations for tqdm
        total_combinations = len(DEVS) * (len(DEVS) - 1) // 2
    
        cols = [
            "name_1",
            "email_1",
            "name_2",
            "email_2",
            "is_duplicate",
        ]

        with open(raw_path, "w", newline="", encoding="utf-8") as rawf:
            writer = csv.writer(rawf)
            writer.writerow(cols)
            combos = combinations(DEVS, 2)
            
            sample = biased_sample(list(combos), num_pairs) # Get a sample of pairs with lots of potential duplicates
            
            for dev1, dev2 in sample:
                name_1, email_1 = dev1
                name_2, email_2 = dev2
                is_dup = 0
                writer.writerow([name_1, email_1, name_2, email_2, is_dup])

            