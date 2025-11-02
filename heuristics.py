from Levenshtein import ratio as sim
import utils

def calculate_similarity_bird(dev_a, dev_b):
    name_a, first_a, last_a, i_first_a, i_last_a, email_a, prefix_a = dev_a
    name_b, first_b, last_b, i_first_b, i_last_b, email_b, prefix_b = dev_b
    
    # Conditions of Bird heuristic
    c1 = sim(name_a, name_b)
    c2 = sim(prefix_b, prefix_a)
    c31 = sim(first_a, first_b)
    c32 = sim(last_a, last_b)
    c4 = c5 = c6 = c7 = False
    
    # Since lastname and initials can be empty, perform appropriate checks
    if i_first_a != "" and last_a != "":
        c4 = i_first_a in prefix_b and last_a in prefix_b
    if i_last_a != "":
        c5 = i_last_a in prefix_b and first_a in prefix_b
    if i_first_b != "" and last_b != "":
        c6 = i_first_b in prefix_a and last_b in prefix_a
    if i_last_b != "":
        c7 = i_last_b in prefix_a and first_b in prefix_a
    return c1, c2, c31, c32, c4, c5, c6, c7

def calculate_similarity_improved(dev_a, dev_b):
    """Calculate similarity conditions between two developers using the improved heuristic.
    Args:
        dev_a (tuple): Processed developer a
        dev_b (tuple): Processed developer b
    Returns:
        tuple: Similarity conditions c1 to c8
    """
    name_a, first_a, last_a, i_first_a, i_last_a, email_a, prefix_a = dev_a
    name_b, first_b, last_b, i_first_b, i_last_b, email_b, prefix_b = dev_b

    # Conditions of improved heuristic
    c1 = utils.name_similarity(first_a, first_b)    # First name similarity
    c2 = utils.name_similarity(last_a, last_b)  # Last name similarity
    c3 = utils.name_similarity(name_a, name_b)  # Full name similarity ( UNUSED AT THE MOMENT )
    c4 = utils.email_similarity(email_a, email_b)  # Email similarity
    
    # Check email prefix matches with initials and names
    c5 = utils.prefix_match(prefix_b, i_first_a, last_a) if i_first_a and last_a else 0.0 
    c6 = utils.prefix_match(prefix_b, i_last_a, first_a) if i_last_a else 0.0
    c7 = utils.prefix_match(prefix_a, i_first_b, last_b) if i_first_b and last_b else 0.0
    c8 = utils.prefix_match(prefix_a, i_last_b, first_b) if i_last_b else 0.0
    
    if c5 is None:
        c5 = 0.0
    if c6 is None:
        c6 = 0.0
    if c7 is None:
        c7 = 0.0
    if c8 is None:
        c8 = 0.0
    
    return c1, c2, c3, c4, c5, c6, c7, c8
    
