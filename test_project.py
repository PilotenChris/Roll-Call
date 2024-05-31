from project import validate_date, validate_email, validate_password
import bcrypt


def test_validate_date() -> None:
    assert validate_date("2000-01-01") == True
    assert validate_date("abc") == False


def test_validate_email() -> None:
    assert validate_email("abc@gmail.com") == True
    assert validate_email("abcgmail.com") == False
    assert validate_email("abc@gmail") == False


def test_validate_password() -> None:
    salt = bcrypt.gensalt()
    hash_pass: bytes = bcrypt.hashpw("DFq398g9&Ddgs".encode("utf-8"), salt)
    assert validate_password("DFq398g9&Ddgs".encode("utf-8"), hash_pass) == True
    assert validate_password("NOq938t3&jow2".encode("utf-8"), hash_pass) == False