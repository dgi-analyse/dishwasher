from dataclasses import dataclass
from datetime import date
from typing import Literal

from dishwasher.standardize import standardize_column_name

FNR_COLUMN_CANDIDATES = {
    "fnr",
    "foedselsnummer",
    "fodselsnummer",
    "fødselsnummer",
    "personnummer",
    "persnr",
    "pers_nr",
    "person_nr",
    "personidentifikator",
    "ident",
    "idnr",
    "id_nr",
    "nin",
    "national_identity_number",
    "norwegian_identity_number",
}

FnrCategory = Literal["missing", "fnr", "dnr", "h_number", "invalid"]


@dataclass(frozen=True)
class FnrResult:
    original: object
    normalized: str | None
    category: FnrCategory
    is_valid: bool
    padded: bool
    birth_date: date | None = None
    message: str | None = None


def normalize_fnr(value: object) -> str | None:
    """Normalize a Norwegian fødselsnummer-like value to digits.

    Handles common Excel issues where leading zero is lost.
    """
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    if text.endswith(".0"):
        text = text[:-2]

    digits = "".join(char for char in text if char.isdigit())

    if not digits:
        return None

    if len(digits) == 10:
        return digits.zfill(11)

    return digits


def was_padded(value: object) -> bool:
    normalized = normalize_fnr(value)

    if normalized is None:
        return False

    original_digits = "".join(char for char in str(value).strip() if char.isdigit())

    return len(original_digits) == 10 and len(normalized) == 11


def is_possible_fnr(value: object) -> bool:
    normalized = normalize_fnr(value)

    return normalized is not None and len(normalized) == 11 and normalized.isdigit()

def find_fnr_columns(columns: list[str]) -> list[str]:
    """Find likely fødselsnummer columns by name."""
    matches = []

    for column in columns:
        standardized = standardize_column_name(column)

        if standardized in FNR_COLUMN_CANDIDATES:
            matches.append(column)

    return matches

def classify_fnr(value: object) -> FnrCategory:
    normalized = normalize_fnr(value)

    if normalized is None:
        return "missing"

    if len(normalized) != 11 or not normalized.isdigit():
        return "invalid"

    day = int(normalized[0:2])
    month = int(normalized[2:4])

    if 1 <= day <= 31 and 1 <= month <= 12:
        return "fnr"

    if 41 <= day <= 71 and 1 <= month <= 12:
        return "dnr"

    if 1 <= day <= 31 and 41 <= month <= 52:
        return "h_number"

    return "invalid"


def validate_fnr(value: object) -> bool:
    """Validate Norwegian fødselsnummer/D-number control digits."""
    normalized = normalize_fnr(value)

    if normalized is None or len(normalized) != 11 or not normalized.isdigit():
        return False

    digits = [int(char) for char in normalized]

    k1_weights = [3, 7, 6, 1, 8, 9, 4, 5, 2]
    k2_weights = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    k1 = 11 - (sum(d * w for d, w in zip(digits[:9], k1_weights, strict=True)) % 11)

    if k1 == 11:
        k1 = 0

    if k1 == 10 or k1 != digits[9]:
        return False

    k2 = 11 - (sum(d * w for d, w in zip(digits[:10], k2_weights, strict=True)) % 11)

    if k2 == 11:
        k2 = 0

    return k2 != 10 and k2 == digits[10]


def inspect_fnr(value: object) -> FnrResult:
    normalized = normalize_fnr(value)
    padded = was_padded(value)
    category = classify_fnr(value)

    if normalized is None:
        return FnrResult(
            original=value,
            normalized=None,
            category="missing",
            is_valid=False,
            padded=False,
            birth_date=None,
            message="Missing value",
        )

    if len(normalized) != 11:
        return FnrResult(
            original=value,
            normalized=normalized,
            category="invalid",
            is_valid=False,
            padded=padded,
            birth_date=None,
            message="Expected 11 digits",
        )

    birth_date = get_birth_date(normalized)
    has_valid_control_digits = validate_fnr(normalized)

    if birth_date is None:
        message = "Invalid birth date or invalid century/individual number combination"
    elif not has_valid_control_digits:
        message = "Invalid control digits"
    else:
        message = None

    return FnrResult(
        original=value,
        normalized=normalized,
        category=category,
        is_valid=birth_date is not None and has_valid_control_digits,
        padded=padded,
        birth_date=birth_date,
        message=message,
    )

def get_birth_date(value: object) -> date | None:
    normalized = normalize_fnr(value)

    if normalized is None or len(normalized) != 11 or not normalized.isdigit():
        return None

    category = classify_fnr(normalized)

    day = int(normalized[0:2])
    month = int(normalized[2:4])
    year = int(normalized[4:6])
    individual_number = int(normalized[6:9])

    if category == "dnr":
        day -= 40

    if category == "h_number":
        month -= 40

    full_year = _resolve_century(year, individual_number)

    if full_year is None:
        return None

    try:
        return date(full_year, month, day)
    except ValueError:
        return None


def _resolve_century(year: int, individual_number: int) -> int | None:
    if 0 <= individual_number <= 499:
        return 1900 + year

    if 500 <= individual_number <= 749 and 54 <= year <= 99:
        return 1800 + year

    if 500 <= individual_number <= 999 and 0 <= year <= 39:
        return 2000 + year

    if 900 <= individual_number <= 999 and 40 <= year <= 99:
        return 1900 + year

    return None


def has_valid_birth_date(value: object) -> bool:
    return get_birth_date(value) is not None
