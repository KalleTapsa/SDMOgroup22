import pytest
from utils import normalize_email, name_similarity, email_similarity, prefix_match, preprocess, is_potential_duplicate, biased_sample


def test_normalize_email():
    """Normalize email by lowercasing and stripping whitespace."""
    email = "Jane.Doe@Example.github.com"
    normalized = normalize_email(email)
    assert normalized[0] == "janedoe"
    assert normalized[1] == ["jane", "doe"]
    assert normalized[2] == "example.github.com"

def test_name_similarity():
    name_a = "John Doe"
    name_b = "Jon Doe"
    sim = name_similarity(name_a, name_b)
    assert 0 <= sim <= 1
    
def test_email_similarity():
    email_a = "Jane.Doe@Example.github.com"
    email_b = "Janet.Doe@Example.github.com"
    sim = email_similarity(email_a, email_b)
    assert 0 <= sim <= 1

def test_prefix_match():
    prefix_a = "jdoe"
    token_a = "j"
    token_b = "doe"
    assert prefix_match(prefix_a, token_a, token_b) == 1.0

def test_prefix_match_partial():
    prefix_a = "jane.doe"
    token_a = "j"
    token_b = "doe"
    assert prefix_match(prefix_a, token_a, token_b) == 0.5

def test_is_potential_duplicate():
    dev_a = ["John Doe", "jdoe@example.com"]
    dev_b = ["Jon Doe", "jondoe@example.com"]
    assert is_potential_duplicate(dev_a, dev_b) == 1.0
