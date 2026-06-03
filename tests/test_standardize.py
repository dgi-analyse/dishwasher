import polars as pl
import pytest

from dishwasher.standardize import (
    make_unique_names,
    standardize_column_name,
    standardize_column_names,
    standardize_empty_values,
    standardize_table,
    strip_string_values,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (" Fødselsdato ", "foedselsdato"),
        ("Org.nr", "org_nr"),
        ("Kommune navn", "kommune_navn"),
        ("År", "aar"),
        ("Økonomi", "oekonomi"),
        ("Kjønn", "kjoenn"),
        ("Antall elever (totalt)", "antall_elever_totalt"),
        ("123 start", "col_123_start"),
        ("", "column"),
        ("   ", "column"),
    ],
)
def test_standardize_column_name(raw, expected):
    assert standardize_column_name(raw) == expected


def test_make_unique_names():
    assert make_unique_names(["navn", "navn", "navn"]) == ["navn", "navn_2", "navn_3"]


def test_standardize_column_names():
    df = pl.DataFrame(
        {
            " Navn ": ["Ada"],
            "Org.nr": ["123456789"],
            "År": [2026],
        }
    )

    result = standardize_column_names(df)

    assert result.columns == ["navn", "org_nr", "aar"]


def test_strip_string_values():
    df = pl.DataFrame({"name": [" Ada ", "Linus "]})

    result = strip_string_values(df)

    assert result["name"].to_list() == ["Ada", "Linus"]


def test_standardize_empty_values():
    df = pl.DataFrame({"name": ["Ada", "", "   "]})

    result = standardize_empty_values(df)

    assert result["name"].to_list() == ["Ada", None, None]


def test_standardize_table_defaults_to_string():
    df = pl.DataFrame(
        {
            " Navn ": [" Ada ", ""],
            "År": [2025, 2026],
        }
    )

    result = standardize_table(df)

    assert result.columns == ["navn", "aar"]
    assert result["navn"].to_list() == ["Ada", None]
    assert result["aar"].dtype == pl.String
    assert result["aar"].to_list() == ["2025", "2026"]


def test_standardize_table_type_mode_none_preserves_types():
    df = pl.DataFrame({"År": [2025, 2026]})

    result = standardize_table(df, type_mode="none")

    assert result["aar"].dtype == pl.Int64
