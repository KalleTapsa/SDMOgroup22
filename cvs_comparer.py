import csv
import os
import pandas as pd
import config

file_path = os.path.join("project1devs", config.TEAM_MEMBER.lower().strip())
# HERE CHANGE WHAT THRESHOLD U USED
bird_path = os.path.join(file_path, "devs_similarity_t=0.65_heuristic=bird.csv")
improved_path = os.path.join(file_path, "devs_similarity_t=0.65_heuristic=improved.csv")

header = ['name_1', 'email_1', 'name_2', 'email_2', 'c1', 'c2', 'c3.1', 'c3.2', 'c4', 'c5', 'c6', 'c7']

def load_csv(path):
    rows = [header]
    with open(path, "r", newline="", encoding="utf-8") as csvfile:
        reader = list(csv.reader(csvfile))
        rows.extend(reader[1:])
    return rows

bird = load_csv(bird_path)
improved = load_csv(improved_path)

bird_users = {tuple(row[:4]) for row in bird[1:]}
improved_users = {tuple(row[:4]) for row in improved[1:]}

bird_unique = [header] + [row for row in bird[1:] if tuple(row[:4]) not in improved_users]
improved_unique = [header] + [row for row in improved[1:] if tuple(row[:4]) not in bird_users]
overlap = [header] + [row for row in bird[1:] if tuple(row[:4]) in improved_users]

def write_sheet(writer, sheet_name, data):
    df = pd.DataFrame(data[1:], columns=header)
    df.to_excel(writer, sheet_name=sheet_name, index=False)

with pd.ExcelWriter(os.path.join(file_path, "cvs_comparison.xlsx")) as writer:
    write_sheet(writer, "bird_unique", bird_unique)
    write_sheet(writer, "improved_unique", improved_unique)
    write_sheet(writer, "overlap", overlap)
