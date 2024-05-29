from project import validate_date, validate_email, validate_password


def test_validate_date() -> None:
    assert validate_date("2000-01-01") == True
    assert validate_date("abc") == False


def test_validate_email() -> None:
    assert validate_email("abc@gmail.com") == True
    assert validate_email("abcgmail.com") == False
    assert validate_email("abc@gmail") == False


def test_validate_password() -> None:
    ...