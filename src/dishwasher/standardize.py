import re
import unicodedata
from typing import Literal

import polars as pl

TypeMode = Literal["string", "infer", "none"]


def standardize_column_name(name: str) -> str:
    """Convert a column name to simple snake_case."""
    value = name.strip().lower()

    # Norwegian transliteration first
    value = (
        value.replace("æ", "ae")
        .replace("ø", "oe")
        .replace("å", "aa")
    )

    # Remove remaining accents/diacritics
    value = unicodedata.normalize("NFKD", value)
    value = "".join(
        char
        for char in value
        if not unicodedata.combining(char)
    )

    value = value.replace("&", " og ")

    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    value = value.strip("_")

    if not value:
        return "column"

    if value[0].isdigit():
        value = f"col_{value}"

    return value


def make_unique_names(names: list[str]) -> list[str]:
    """Ensure column names are unique."""
    seen: dict[str, int] = {}
    result: list[str] = []

    for name in names:
        count = seen.get(name, 0)

        if count == 0:
            result.append(name)
        else:
            result.append(f"{name}_{count + 1}")

        seen[name] = count + 1

    return result


def standardize_column_names(df: pl.DataFrame) -> pl.DataFrame:
    """Standardize all column names."""
    names = [standardize_column_name(name) for name in df.columns]
    unique_names = make_unique_names(names)

    return df.rename(dict(zip(df.columns, unique_names, strict=True)))


def standardize_empty_values(df: pl.DataFrame) -> pl.DataFrame:
    """Convert empty strings and whitespace-only strings to null."""
    expressions = []

    for name, dtype in df.schema.items():
        if dtype == pl.String:
            expressions.append(
                pl.when(pl.col(name).str.strip_chars() == "")
                .then(None)
                .otherwise(pl.col(name))
                .alias(name)
            )
        else:
            expressions.append(pl.col(name))

    return df.with_columns(expressions)


def strip_string_values(df: pl.DataFrame) -> pl.DataFrame:
    """Strip leading and trailing whitespace from string columns."""
    expressions = []

    for name, dtype in df.schema.items():
        if dtype == pl.String:
            expressions.append(pl.col(name).str.strip_chars().alias(name))
        else:
            expressions.append(pl.col(name))

    return df.with_columns(expressions)


def cast_all_to_string(df: pl.DataFrame) -> pl.DataFrame:
    """Cast all columns to string."""
    return df.with_columns([pl.col(name).cast(pl.String).alias(name) for name in df.columns])


def standardize_table(df: pl.DataFrame, *, type_mode: TypeMode = "string") -> pl.DataFrame:
    """Standardize a table for predictable analysis."""
    df = standardize_column_names(df)
    df = strip_string_values(df)
    df = standardize_empty_values(df)

    if type_mode == "string":
        return cast_all_to_string(df)

    if type_mode == "infer":
        return df

    if type_mode == "none":
        return df

    raise ValueError(f"Unknown type_mode: {type_mode}")
