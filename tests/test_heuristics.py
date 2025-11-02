import pytest
from unittest.mock import patch
from heuristics import calculate_similarity_bird, calculate_similarity_improved
from utils import preprocess


def mock_sim(a, b):
    """Simple mock similarity function that returns 1.0 if identical, else 0.0"""
    return 1.0 if a.lower() == b.lower() else 0.0


@pytest.fixture(autouse=True)
def patch_sim(monkeypatch):
    monkeypatch.setattr("heuristics.sim", mock_sim)


def test_identical_devs_bird():
    dev_a = preprocess(["John Smith", "john.smith@gmail.com"])
    dev_b = preprocess(["John Smith", "john.smith@gmail.com"])

    c1, c2, c31, c32, c4, c5, c6, c7 = calculate_similarity_bird(dev_a, dev_b)
    assert c1 == 1.0
    assert c2 == 1.0
    assert c31 == 1.0
    assert c32 == 1.0
    assert all(isinstance(c, bool) for c in (c4, c5, c6, c7))
    assert all(c for c in (c4, c5, c6, c7)) is True


def test_almost_identical_devs_bird():
    dev_a = preprocess(["John Smith", "john.smith@gmail.com"])
    dev_b = preprocess(["John Smith", "jsmith@gmail.com"])
    c1, c2, c31, c32, c4, c5, c6, c7 = calculate_similarity_bird(dev_a, dev_b)
    assert c1 == 1.0
    assert c2 == 0.0
    assert c31 == 1.0
    assert c32 == 1.0
    assert c4 is True
    assert c5 is False
    assert c6 is True
    assert c7 is True


def test_different_devs_bird():
    dev_a = preprocess(["John Smith", "john.smith@gmail.com"])
    dev_b = preprocess(["Linus Torvalds", "linus@linux.com"])
    c1, c2, c31, c32, c4, c5, c6, c7 = calculate_similarity_bird(dev_a, dev_b)
    assert all(c == 0 for c in (c1, c2, c31, c32))
    assert all(c is False for c in (c4, c5, c6, c7))


def test_prefix_initial_lastname_match_bird():
    dev_a = preprocess(["John Smith", "john.smith@gmail.com"])
    dev_b = preprocess(["J. Smith", "jsmith@gmail.com"])

    c1, c2, c31, c32, c4, c5, c6, c7 = calculate_similarity_bird(dev_a, dev_b)

    # Verify the prefix logic
    assert c4 is True
    assert c5 is False
    assert c6 is False
    assert c7 is True


def test_missing_values_bird():
    dev_a = ("", "", "", "", "", "", "")
    dev_b = preprocess(["John Smith", "john.smith@gmail.com"])
    c1, c2, c31, c32, c4, c5, c6, c7 = calculate_similarity_bird(dev_a, dev_b)

    # Should safely produce zeros/False, not crash or return None
    assert all(isinstance(c, float) for c in (c1, c2, c31, c32))
    assert all(isinstance(c, bool) for c in (c4, c5, c6, c7))
    assert all(c == 0.0 for c in (c1, c2, c31, c32))
    assert all(c is False for c in (c4, c5, c6, c7))


@pytest.fixture(autouse=True)
def patch_name_similarity(monkeypatch):
    monkeypatch.setattr("heuristics.utils.name_similarity", mock_sim)


@pytest.fixture(autouse=True)
def patch_email_similarity(monkeypatch):
    monkeypatch.setattr("heuristics.utils.email_similarity", mock_sim)


def mock_prefix_match(prefix, *tokens):
    combined = "".join(tokens).lower()
    if prefix == combined:
        return 1.0
    else:
        return 0.0


@pytest.fixture(autouse=True)
def patch_prefix_match(monkeypatch):
    monkeypatch.setattr("heuristics.utils.prefix_match", mock_prefix_match)


def test_identical_devs_improved():
    dev_a = preprocess(["John Smith", "john.smith@gmail.com"])
    dev_b = preprocess(["John Smith", "john.smith@gmail.com"])
    c11, c12, c2, c3, c4, c5, c6, c7 = calculate_similarity_improved(dev_a, dev_b)
    assert all(c == 1.0 for c in (c11, c12, c2, c3))
    assert all(c == 0.0 for c in (c4, c5, c6, c7))


def test_almost_identical_devs_improved():
    dev_a = preprocess(["John Smith", "john.smith@gmail.com"])
    dev_b = preprocess(["J. Smith", "jsmith@gmail.com"])
    c11, c12, c2, c3, c4, c5, c6, c7 = calculate_similarity_improved(dev_a, dev_b)
    assert c11 == 0.0
    assert c12 == 1.0
    assert c2 == 0.0
    assert c3 == 0.0
    assert c4 == 1.0
    assert c5 == 0.0
    assert c6 == 0.0
    assert c7 == 0.0


def test_different_devs_improved():
    dev_a = preprocess(["John Smith", "john.smith@gmail.com"])
    dev_b = preprocess(["Linus Torvalds", "linus@linux.com"])
    c11, c12, c2, c3, c4, c5, c6, c7 = calculate_similarity_improved(dev_a, dev_b)
    assert all(c == 0.0 for c in (c11, c12, c2, c3, c4, c5, c6, c7))


def test_missing_values_improved():
    dev_a = ("", "", "", "", "", "", "")
    dev_b = preprocess(["John Smith", "john.smith@gmail.com"])
    c11, c12, c2, c3, c4, c5, c6, c7 = calculate_similarity_improved(dev_a, dev_b)
    # Should safely produce zeros, not crash or return None
    assert all(isinstance(c, float) for c in (c11, c12, c2, c3, c4, c5, c6, c7))
    assert all(c == 0.0 for c in (c11, c12, c2, c3, c4, c5, c6, c7))
