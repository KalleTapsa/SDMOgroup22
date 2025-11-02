import csv
import os
import sys
from tqdm import tqdm
import config
from itertools import combinations
from heuristics import calculate_similarity_bird, calculate_similarity_improved
from utils import preprocess
import pandas as pd
import argparse

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Calculate developer similarities using specified heuristic."
    )
    argparser.add_argument(
        "--heuristic",
        type=str,
        choices=["bird", "improved"],
        required=True,
        help="Heuristic to use for similarity calculation",
    )
    argparser.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        required=False,
        help="Similarity threshold for determining duplicates (default: 0.7)",
    )
    args = argparser.parse_args()
    heuristic = args.heuristic
    threshold = args.threshold

    csv_file_path = os.path.join("project1devs", config.TEAM_MEMBER.lower().strip())
    raw_path = os.path.join(csv_file_path, f"devs_similarity_raw_{heuristic}.csv")

    if not os.path.isfile(raw_path):
        devs_file_path = os.path.join(csv_file_path, "devs.csv")
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

        cols = []
        if heuristic == "bird":
            cols = [
                "name_1",
                "email_1",
                "name_2",
                "email_2",
                "c1",
                "c2",
                "c3.1",
                "c3.2",
                "c4",
                "c5",
                "c6",
                "c7",
            ]
        elif heuristic == "improved":
            cols = [
                "name_1",
                "email_1",
                "name_2",
                "email_2",
                "c11",
                "c12",
                "c2",
                "c3",
                "c4",
                "c5",
                "c6",
                "c7",
            ]

        # Total combinations for tqdm
        total_combinations = len(DEVS) * (len(DEVS) - 1) // 2

        # Stream the similarities to a csv file to avoid running out of memory with a big dataset
        with open(raw_path, "w", newline="", encoding="utf-8") as rawf:
            writer = csv.writer(rawf)
            writer.writerow(cols)
            combos = combinations(DEVS, 2)
            for dev_a, dev_b in tqdm(
                combos, total=total_combinations, desc="Processing dev combinations"
            ):
                # Pre-process both developers
                (name_a, first_a, last_a, i_first_a, i_last_a, email_a, prefix_a) = (
                    preprocess(dev_a)
                )
                (name_b, first_b, last_b, i_first_b, i_last_b, email_b, prefix_b) = (
                    preprocess(dev_b)
                )

                if heuristic == "bird":
                    # Calculate similarity conditions
                    c1, c2, c31, c32, c4, c5, c6, c7 = calculate_similarity_bird(
                        (
                            name_a,
                            first_a,
                            last_a,
                            i_first_a,
                            i_last_a,
                            email_a,
                            prefix_a,
                        ),
                        (
                            name_b,
                            first_b,
                            last_b,
                            i_first_b,
                            i_last_b,
                            email_b,
                            prefix_b,
                        ),
                    )
                    # Write results to csv
                    writer.writerow(
                        [
                            dev_a[0],
                            email_a,
                            dev_b[0],
                            email_b,
                            c1,
                            c2,
                            c31,
                            c32,
                            c4,
                            c5,
                            c6,
                            c7,
                        ]
                    )
                elif heuristic == "improved":
                    # Calculate similarity conditions
                    c11, c12, c2, c3, c4, c5, c6, c7 = calculate_similarity_improved(
                        (
                            name_a,
                            first_a,
                            last_a,
                            i_first_a,
                            i_last_a,
                            email_a,
                            prefix_a,
                        ),
                        (
                            name_b,
                            first_b,
                            last_b,
                            i_first_b,
                            i_last_b,
                            email_b,
                            prefix_b,
                        ),
                    )
                    # Write results to csv
                    writer.writerow(
                        [dev_a[0], email_a, dev_b[0], email_b, c11, c12, c2, c3, c4, c5, c6, c7]
                    )

    # Read dataframe from csv
    df = pd.read_csv(raw_path, low_memory=False)

    # Set similarity threshold, check c1-c3 against the threshold
    print("Threshold:", threshold)
    if heuristic == "bird":
        df["c1_check"] = df["c1"] >= threshold
        df["c2_check"] = df["c2"] >= threshold
        df["c3_check"] = (df["c3.1"] >= threshold) & (df["c3.2"] >= threshold)
        # Keep only rows where at least one condition is True
        df = df[
            df[["c1_check", "c2_check", "c3_check", "c4", "c5", "c6", "c7"]].any(axis=1)
        ]

        # Omit "check" columns, save to csv
        df = df[
            [
                "name_1",
                "email_1",
                "name_2",
                "email_2",
                "c1",
                "c2",
                "c3.1",
                "c3.2",
                "c4",
                "c5",
                "c6",
                "c7",
            ]
        ]
    elif heuristic == "improved":
        df["c1_check"] = (df["c11"] >= threshold) & (df["c12"] >= threshold)
        df["c2_check"] = df["c2"] >= threshold
        df["c3_check"] = df["c3"] >= threshold
        df["c4_check"] = df["c4"] >= threshold
        df["c5_check"] = df["c5"] >= threshold
        df["c6_check"] = df["c6"] >= threshold
        df["c7_check"] = df["c7"] >= threshold
        
        # Keep only rows where at least one condition is True
        df = df[
            df[["c1_check", "c2_check", "c3_check", "c4_check", "c5_check", "c6_check", "c7_check"]].any(axis=1)
        ]
        
        # Omit "check" columns, save to csv
        df = df[["name_1", "email_1", "name_2", "email_2", "c11", "c12", "c2", "c3", "c4", "c5", "c6", "c7"]]
        
    # Added a print to see how many duplicates are found
    print(f"{len(df)} duplicates found")
    df.to_csv(
        os.path.join(csv_file_path, f"devs_similarity_t={threshold}_heuristic={heuristic}.csv"),
        index=False,
        header=True,
    )
