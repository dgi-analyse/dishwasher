from pathlib import Path

import polars as pl

SUPPORTED_EXTENSIONS = {
    ".csv",
    ".tsv",
    ".txt",
    ".xlsx",
    ".xls",
    ".parquet",
    ".json",
    ".jsonl",
    ".ndjson",
}


def read_table(path: str | Path, *, sheet_name: str | None = None) -> pl.DataFrame:
    """Read a tabular file into a Polars DataFrame.

    Supported formats:
    - CSV
    - TSV
    - Excel
    - Parquet
    - JSON / NDJSON
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(f"Unsupported file type: {suffix}. Supported types: {supported}")

    if suffix == ".csv":
        return pl.read_csv(file_path)

    if suffix in {".tsv", ".txt"}:
        return pl.read_csv(file_path, separator="\t")

    if suffix in {".xlsx", ".xls"}:
        if sheet_name is None:
            return pl.read_excel(file_path)
        return pl.read_excel(file_path, sheet_name=sheet_name)

    if suffix == ".parquet":
        return pl.read_parquet(file_path)

    if suffix == ".json":
        return pl.read_json(file_path)

    if suffix in {".jsonl", ".ndjson"}:
        return pl.read_ndjson(file_path)

    raise ValueError(f"Unsupported file type: {suffix}")
