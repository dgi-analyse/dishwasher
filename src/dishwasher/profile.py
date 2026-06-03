from dataclasses import dataclass
from pathlib import Path

from dishwasher.io import read_table


@dataclass(frozen=True)
class ColumnProfile:
    name: str
    dtype: str
    null_count: int
    unique_count: int


@dataclass(frozen=True)
class ProfileResult:
    path: Path
    rows: int
    columns: int
    column_profiles: list[ColumnProfile]


def profile_file(path: str | Path) -> ProfileResult:
    file_path = Path(path)
    df = read_table(file_path)

    profiles = [
        ColumnProfile(
            name=name,
            dtype=str(df.schema[name]),
            null_count=df[name].null_count(),
            unique_count=df[name].n_unique(),
        )
        for name in df.columns
    ]

    return ProfileResult(
        path=file_path,
        rows=df.height,
        columns=df.width,
        column_profiles=profiles,
    )
