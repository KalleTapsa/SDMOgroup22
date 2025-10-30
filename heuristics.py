from Levenshtein import ratio as sim


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
    name_a, first_a, last_a, i_first_a, i_last_a, email_a, prefix_a = dev_a
    name_b, first_b, last_b, i_first_b, i_last_b, email_b, prefix_b = dev_b

    email_postfix_a = email_a.split("@")[1] if "@" in email_a else email_a
    email_postfix_b = email_b.split("@")[1] if "@" in email_b else email_b

    # Conditions of edited heuristic
    c1 = sim(name_a, name_b)
    c2 = sim(prefix_a, prefix_b) * sim(email_postfix_a, email_postfix_b)
    c31 = sim(first_a, first_b)
    c32 = sim(last_a, last_b)

    return c1, c2, c31, c32
