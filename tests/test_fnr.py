from datetime import date

from dishwasher.fnr import (
    classify_fnr,
    find_fnr_columns,
    inspect_fnr,
    is_possible_fnr,
    normalize_fnr,
    validate_fnr,
    was_padded,
)


def test_find_fnr_columns():
    columns = ["Navn", "Fødselsnummer", "Adresse", "pers_nr"]

    assert find_fnr_columns(columns) == ["Fødselsnummer", "pers_nr"]

def test_normalize_fnr_keeps_11_digits():
    assert normalize_fnr("01010112345") == "01010112345"


def test_normalize_fnr_pads_10_digits():
    assert normalize_fnr("1010112345") == "01010112345"


def test_normalize_fnr_removes_separators():
    assert normalize_fnr("010101-12345") == "01010112345"
    assert normalize_fnr("010101 12345") == "01010112345"


def test_normalize_fnr_handles_excel_float_string():
    assert normalize_fnr("1010112345.0") == "01010112345"


def test_normalize_fnr_missing_values():
    assert normalize_fnr(None) is None
    assert normalize_fnr("") is None
    assert normalize_fnr("   ") is None


def test_was_padded():
    assert was_padded("1010112345") is True
    assert was_padded("01010112345") is False


def test_is_possible_fnr():
    assert is_possible_fnr("01010112345") is True
    assert is_possible_fnr("123") is False


def test_classify_fnr():
    assert classify_fnr(None) == "missing"
    assert classify_fnr("01010112345") == "fnr"
    assert classify_fnr("41010112345") == "dnr"
    assert classify_fnr("01410112345") == "h_number"
    assert classify_fnr("99139912345") == "invalid"


def test_validate_fnr_known_valid_example():
    # Common test number with valid control digits.
    assert validate_fnr("01010101006") is True


def test_validate_fnr_invalid_control_digits():
    assert validate_fnr("01010101007") is False


def test_inspect_fnr():
    result = inspect_fnr("1010101006")

    assert result.normalized == "01010101006"
    assert result.category == "fnr"
    assert result.is_valid is True
    assert result.padded is True

def test_get_birth_date_fnr_1900s():
    from dishwasher.fnr import get_birth_date

    assert get_birth_date("01010101006") == date(1901, 1, 1)


def test_get_birth_date_dnr():
    from dishwasher.fnr import get_birth_date

    assert get_birth_date("41010101006") == date(1901, 1, 1)


def test_get_birth_date_h_number():
    from dishwasher.fnr import get_birth_date

    assert get_birth_date("01410101006") == date(1901, 1, 1)


def test_invalid_birth_date_returns_none():
    from dishwasher.fnr import get_birth_date

    assert get_birth_date("99139912345") is None
