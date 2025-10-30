import pytest
from unittest.mock import patch
from heuristics import calculate_similarity_bird, calculate_similarity_improved


@pytest.fixture
def devs():
    dev_a = ("john doe", "john", "doe", "j", "d", "john.doe@example.com", "john.doe")
    dev_b = ("jane doe", "jane", "doe", "j", "d", "jane.doe@example.com", "jane.doe")
    return dev_a, dev_b


@patch("heuristics.sim")
def test_similarity_conditions_bird(mock_sim, devs):
    dev_a, dev_b = devs
    # Make all similarity checks return False by default
    mock_sim.return_value = False

    result = calculate_similarity_bird(dev_a, dev_b)
    assert result == (False, False, False, False, True, False, True, False)
    assert mock_sim.call_count == 4 


@patch("heuristics.sim")
def test_some_similarities_true_bird(mock_sim, devs):
    dev_a, dev_b = devs

    mock_sim.side_effect = [True, False, True, False]

    result = calculate_similarity_bird(dev_a, dev_b)

    expected_results = (True, False, True, False, True, False, True, False)
    assert result == expected_results


@patch("heuristics.sim")
def test_missing_initials_and_lastname_bird(mock_sim):
    dev_a = ("john", "john", "", "j", "", "john@example.com", "john")
    dev_b = ("jane", "jane", "", "j", "", "jane@example.com", "jane")

    mock_sim.side_effect = [True, True, True, True]

    result = calculate_similarity_bird(dev_a, dev_b)

    # c4–c7 should all be False because last names and initials are missing
    assert result == (True, True, True, True, False, False, False, False)

@patch("heuristics.sim")
def test_similarity_conditions_improved(mock_sim, devs):
    dev_a, dev_b = devs
    # Make all similarity checks return False by default
    mock_sim.return_value = False

    result = calculate_similarity_improved(dev_a, dev_b)
    assert result == (False, False, False, False)
    assert mock_sim.call_count == 5


@patch("heuristics.sim")
def test_some_similarities_true_improved(mock_sim, devs):
    dev_a, dev_b = devs

    mock_sim.side_effect = [True, False, False, True, False]    # Set some of the returns to true

    result = calculate_similarity_improved(dev_a, dev_b)

    assert result == (True, False, True, False)


@patch("heuristics.sim")
def test_invalid_emails_improved(mock_sim, devs):
    dev_a, dev_b = devs
    dev_a = list(dev_a)
    dev_b = list(dev_b)

    # Set invalid emails
    dev_a[5] = "6"
    dev_b[5] = "7"

    mock_sim.side_effect = [True, True, True, True, True]

    result = calculate_similarity_improved(tuple(dev_a), tuple(dev_b))

    assert result == (True, True, True, True)