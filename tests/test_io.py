import polars as pl
import pytest

from dishwasher.io import read_table


def test_read_csv(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("name,age\nAda,36\nLinus,55\n", encoding="utf-8")

    df = read_table(path)

    assert df.shape == (2, 2)
    assert df.columns == ["name", "age"]


def test_read_tsv(tmp_path):
    path = tmp_path / "data.tsv"
    path.write_text("name\tage\nAda\t36\nLinus\t55\n", encoding="utf-8")

    df = read_table(path)

    assert df.shape == (2, 2)
    assert df.columns == ["name", "age"]


def test_read_parquet(tmp_path):
    path = tmp_path / "data.parquet"
    original = pl.DataFrame({"name": ["Ada", "Linus"], "age": [36, 55]})
    original.write_parquet(path)

    df = read_table(path)

    assert df.shape == (2, 2)
    assert df.columns == ["name", "age"]


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        read_table("does-not-exist.csv")


def test_unsupported_file_type_raises(tmp_path):
    path = tmp_path / "data.docx"
    path.write_text("not a table", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type"):
        read_table(path)


def test_read_excel(tmp_path):
    path = tmp_path / "data.xlsx"

    original = pl.DataFrame(
        {
            "name": ["Ada", "Linus"],
            "age": [36, 55],
        }
    )

    original.write_excel(path)

    df = read_table(path)

    assert df.shape == (2, 2)
    assert df.columns == ["name", "age"]
