import string
import unicodedata
from rapidfuzz import fuzz
import numpy as np

def normalize_email(email):
    """Normalize email by extracting prefix and domain.
    Args:
        email (string): email address
    Returns:
        tuple: entire prefix without dots, list of prefix parts split by dots, domain
    """
    email = email.strip().lower()
    prefix, _, domain = email.partition("@")
    prefix_whole = prefix.replace(".", "")
    prefix_split = prefix.split(".")
    return prefix_whole, prefix_split, domain

def name_similarity(name_a, name_b):
    """Calculate the similarity between two names using token sort ratio from rapidfuzz.
    Args:
        name_a (string): name 1
        name_b (string): name 2
    Returns:
        float: similarity score between 0 and 1
    """
    if not name_a or not name_b:
        return 0.0
    return fuzz.token_sort_ratio(name_a.lower(), name_b.lower()) / 100.0

def email_similarity(e1, e2):
    """Calculate the similarity between two emails based on prefix and domain.
    Args:
        e1 (string): email 1
        e2 (string): email 2
    Returns:
        float: similarity score between 0 and 1
    """
    if not e1 or not e2:
        return 0.0
    p1, _, d1 = normalize_email(e1)
    p2, _, d2 = normalize_email(e2)
    if d1 == d2:
        domain_score = 1.0
    elif d1.split('.')[-1] == d2.split('.')[-1]:
        domain_score = 0.5
    else:
        domain_score = 0.0
    prefix_score = fuzz.ratio(p1, p2) / 100.0
    return 0.85 * prefix_score + 0.15 * domain_score

def prefix_match(prefix, *tokens):
    """Check if all tokens are present in the prefix and calculate a match score.
    Args:
        prefix (string): email prefix
        *tokens (string): tokens to check in the prefix
    Returns:
        float: match score between 0 and 1
    """
    if not prefix or not tokens:
        return 0.0
    p = prefix.lower()
    if all(tok.lower() in p for tok in tokens if tok):
        combined = "".join(tokens).lower()
        if p == combined:
            return 1.0
        else:
            return min(len(combined) / len(p), 1)
            

def preprocess(dev):
    """
    Pre-process developer name and email for similarity comparison.
    Args:
        dev: List containing [name, email]
    Returns:
        Tuple of processed (name, first name, last name, initial first, initial last, email, email prefix)
    """
    name: str = dev[0]

    # Remove punctuation
    trans = name.maketrans("", "", string.punctuation)
    name = name.translate(trans)
    # Remove accents, diacritics
    name = unicodedata.normalize("NFKD", name)
    name = "".join([c for c in name if not unicodedata.combining(c)])
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

    # Take initials of firstname and lastname if they are long enough
    i_first = first[0] if len(first) > 1 else ""
    i_last = last[0] if len(last) > 1 else ""

    # Determine email prefix
    email: str = dev[1]
    prefix = email.split("@")[0]

    return name, first, last, i_first, i_last, email, prefix


def is_potential_duplicate(dev_a, dev_b):
    """Simple heuristic to determine if two developers are potential duplicates based on name and email similarity.
    Args:
        dev_a (tuple): name, email
        dev_b (tuple): name, email
    Returns:
        bool: True if potential duplicates, False otherwise
    """
    name_a, _, _, _, _, email_a, prefix_a = preprocess(dev_a)
    name_b, _, _, _, _, email_b, prefix_b = preprocess(dev_b)
    
    name_similarity = fuzz.token_sort_ratio(name_a, name_b) / 100.0
    email_similarity = fuzz.token_sort_ratio(prefix_a, prefix_b) / 100.0
    
    return name_similarity >= 0.7 or email_similarity >= 0.7
