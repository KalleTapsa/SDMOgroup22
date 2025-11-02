import pandas as pd
from heuristics import calculate_similarity_bird, calculate_similarity_improved
from utils import preprocess
from sklearn.metrics import precision_score, recall_score, f1_score
import argparse


def score_bird(dev_a, dev_b, threshold):
    """Calculate the bird similarity between two devs and return whether or not the pair is a duplicate based on a set threshold.
    Args:
        dev_a (tuple): first developer
        dev_b (tuple): second developer
        threshold (flaot): threshold for determining duplicates
    Returns:
        bool: True if duplicate, False otherwise
    """
    c1, c2, c31, c32, c4, c5, c6, c7 = calculate_similarity_bird(dev_a, dev_b)
    return (
        (c1 >= threshold)
        or (c2 >= threshold)
        or ((c31 >= threshold) and (c32 >= threshold))
        or c4
        or c5
        or c6
        or c7
    )


def score_improved(dev_a, dev_b, threshold):
    """Calculate the similarity between two devs using the improved heuristic and return whether or not the pair is a duplicate based on a set threshold.
    Args:
        dev_a (tuple): first developer
        dev_b (tuple): second developer
        threshold (flaot): threshold for determining duplicates
    Returns:
        bool: True if duplicate, False otherwise
    """
    c11, c12, c2, c3, c4, c5, c6, c7 = calculate_similarity_improved(dev_a, dev_b)
    return (
        ((c11 >= threshold) and (c12 >= threshold))
        or (c2 >= threshold)
        or (c3 >= threshold)
        or (c4 >= threshold)
        or (c5 >= threshold)
        or (c6 >= threshold)
        or (c7 >= threshold)
    )


def evaluate(validation_csv, threshold=0.7):
    """Evaluate the heuristics on a labeled validation dataset and print precision, recall, and F1-score.
    Args:
        validation_csv (str): Path to the labeled validation CSV file
        threshold (float): Threshold for determining duplicates
    """
    df = pd.read_csv(validation_csv)

    bird_preds = []
    improved_preds = []
    y_true = df["is_duplicate"].astype(int)

    for i, row in df.iterrows():
        name_a, email_a = row["name_1"], row["email_1"]
        name_b, email_b = row["name_2"], row["email_2"]

        dev_a = preprocess((name_a, email_a))
        dev_b = preprocess((name_b, email_b))

        bird_pred = score_bird(dev_a, dev_b, threshold)
        improved_pred = score_improved(dev_a, dev_b, threshold)
        
        true_label = int(row["is_duplicate"])

        if improved_pred != true_label or bird_pred != true_label:
            print(f"Disagreement on row {i}:")
            print(f"  Dev A: {name_a}, {email_a}")
            print(f"  Dev B: {name_b}, {email_b}")
            print(f"  True label: {true_label}")
            print(f"  Bird prediction: {bird_pred}")
            print(f"  Improved prediction: {improved_pred}")

        bird_preds.append(bird_pred)
        improved_preds.append(improved_pred)

    # Compute metrics
    for name, preds in [("Bird", bird_preds), ("Improved", improved_preds)]:
        prec = precision_score(y_true, preds)
        rec = recall_score(y_true, preds)
        f1 = f1_score(y_true, preds)
        print(f"{name} heuristic:")
        print(f"  Precision = {prec:.3f}")
        print(f"  Recall    = {rec:.3f}")
        print(f"  F1-score  = {f1:.3f}")
        print("-" * 40)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate heuristics on a labeled test dataset."
    )
    parser.add_argument(
        "--validation_csv",
        type=str,
        required=True,
        help="Path to the labeled validation CSV file.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="Threshold for determining duplicates (default: 0.7).",
    )
    args = parser.parse_args()
    evaluate(args.validation_csv, threshold=args.threshold)
