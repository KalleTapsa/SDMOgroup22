from preprocess import preprocess


def test_simple_name_and_email():
    dev = ["John Doe", "john.doe@example.com"]
    result = preprocess(dev)
    assert result[0] == "john doe"  # processed name
    assert result[1] == "john"  # first name
    assert result[2] == "doe"  # last name
    assert result[3] == "j"  # initial first
    assert result[4] == "d"  # initial last
    assert result[5] == "john.doe@example.com"  # email
    assert result[6] == "john.doe"  # email prefix


def test_name_with_punctuation():
    dev = ["John Doe!!!", "JD@example.com"]
    result = preprocess(dev)
    assert result[0] == "john doe"  # processed name
    assert result[1] == "john"  # first name
    assert result[2] == "doe"  # last name


def test_name_with_accents():
    dev = ["Mâttì Mëikäläinen", "mm@test.fi"]
    result = preprocess(dev)
    assert result[0] == "matti meikalainen"  # processed name
    assert result[1] == "matti"  # first name
    assert result[2] == "meikalainen"  # last name


def test_name_with_whitespace():
    dev = ["       Jane                Smith       ", ""]
    result = preprocess(dev)
    assert result[0] == "jane smith"  # processed name
    assert result[1] == "jane"  # first name
    assert result[2] == "smith"  # last name


def test_single_name():
    dev = ["Joe", "joe@joe.joe"]
    result = preprocess(dev)
    assert result[0] == "joe"  # processed name
    assert result[1] == "joe"  # first name
    assert result[2] == ""  # last name
    assert result[3] == "j"  # initial first
    assert result[4] == ""  # initial last


def test_multiple_last_names():
    dev = ["Joe Test McTester", "jtmct@test.gov"]
    result = preprocess(dev)
    assert result[0] == "joe test mctester"  # processed name
    assert result[1] == "joe"  # first name
    assert result[2] == "test mctester"  # last name
    assert result[3] == "j"  # initial first
    assert result[4] == "t"  # initial last


def test_empty_name():
    dev = ["", ""]
    result = preprocess(dev)
    assert result[0] == ""  # processed name
    assert result[1] == ""  # first name
    assert result[2] == ""  # last name
    assert result[3] == ""  # initial first
    assert result[4] == ""  # initial last


def test_name_with_only_punctuation():
    dev = ["!!!", ""]
    result = preprocess(dev)
    assert result[0] == ""  # processed name
    assert result[1] == ""  # first name
    assert result[2] == ""  # last name
    assert result[3] == ""  # initial first
    assert result[4] == ""  # initial last


def test_email_prefix():
    dev = ["Joe Biden", "Joe.Biden@usa.gov"]
    result = preprocess(dev)
    assert result[-1] == "Joe.Biden"  # email prefix
