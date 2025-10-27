import csv
import pandas as pd
import unicodedata
import string
from itertools import combinations
from Levenshtein import ratio as sim
import os
import sys
from tqdm import tqdm
from config import *


# Function for pre-processing each name,email
def process(dev):
    name: str = dev[0]

    # Remove punctuation
    trans = name.maketrans("", "", string.punctuation)
    name = name.translate(trans)
    # Remove accents, diacritics
    name = unicodedata.normalize('NFKD', name)
    name = ''.join([c for c in name if not unicodedata.combining(c)])
    # Lowercase
    name = name.casefold()
    # Strip whitespace
    name = " ".join(name.split())


    # Attempt to split name into firstname, lastname by space
    parts = name.split(" ")
    # Expected case
    if len(parts) == 2:
        first, last = parts
    # If there is no space, firstname is full name, lastname empty
    elif len(parts) == 1:
        first, last = name, ""
    # If there is more than 1 space, firstname is until first space, rest is lastname
    else:
        first, last = parts[0], " ".join(parts[1:])

    # Initials from names, changed that one letter can be a factor that determines the same name.
    i_first = first[0] if len(first) >= 1 else ""
    i_last = last[0] if len(last) >= 1 else ""

    # Determine email prefix
    email: str = dev[1]
    prefix = email.split("@")[0]

    return name, first, last, i_first, i_last, email, prefix

if __name__ == "__main__":
    csv_file_path = os.path.join("project1devs", TEAM_MEMBER.lower().strip())
    raw_path = os.path.join(csv_file_path, "devs_similarity_raw.csv")

    if not os.path.isfile(raw_path):
        devs_file_path = os.path.join(csv_file_path, 'devs.csv')
        if not os.path.isfile(devs_file_path):
            print(f"No csv file found at {devs_file_path}! First use fetch_devs.py to generate it.")
            sys.exit()
        
        DEVS = []
        # Read csv file with name,dev columns
        with open(devs_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                DEVS.append(row)
        # First element is header, skip
        DEVS = DEVS[1:]
        
        cols = ["name_1", "email_1", "name_2", "email_2", "c1", "c2",
                "c3.1", "c3.2"]

        # Total combinations for tqdm
        total_combinations = len(DEVS) * (len(DEVS) - 1) // 2

        # Stream the similarities to a csv file to avoid running out of memory with a big dataset
        with open(raw_path, "w", newline="", encoding="utf-8") as rawf:
            writer = csv.writer(rawf)
            writer.writerow(cols)
            combos = combinations(DEVS, 2)
            for dev_a, dev_b in tqdm(combos, total=total_combinations, desc="Processing dev combinations"):
                # Developer pre-prosessing
                name_a, first_a, last_a, i_first_a, i_last_a, email_a, prefix_a = process(dev_a)
                name_b, first_b, last_b, i_first_b, i_last_b, email_b, prefix_b = process(dev_b)
                # Conditions of edited heuristic
                c1 = sim(name_a, name_b)
                c2 = sim(prefix_a, prefix_b) * sim(email_a.split('@')[1], email_b.split('@')[1])
                c31 = sim(first_a, first_b)
                c32 = sim(last_a, last_b)

                writer.writerow([dev_a[0], email_a, dev_b[0], email_b, c1, c2, c31, c32])

    # Read dataframe from csv
    df = pd.read_csv(raw_path, low_memory=False)

    # Similarity threshold value is at 0.7, as the conditions are tighter otherwise. If only one part is over the threshold, raisinig the 
    # similarity threshold gives better results. After experimenting 0.7 was found to give the best results

    t = 0.7


    print("Threshold:", t)
    

    df["c_sum"] = (

    (df["c1"] >= t).astype(int) +
    (df["c2"] >= t).astype(int) +
    ((df["c3.1"] >= t) & (df["c3.2"] >= t)).astype(int)
)

# Rows that have two parts over threshold are kept
df = df[df["c_sum"] >= 2]


# Omit "check" columns, save to csv
df = df[["name_1", "email_1", "name_2", "email_2", "c1", "c2",
            "c3.1", "c3.2"]]
    
# Added a print to see how many duplicates are found
print(f"{len(df)} duplicates found")
df.to_csv(os.path.join(csv_file_path, f"devs_similarity_t={t}.csv"), index=False, header=True)