from dataclasses import dataclass
from pathlib import Path

from dishwasher.io import read_table


@dataclass(frozen=True)
class InspectionResult:
    path: Path
    rows: int
    columns: int
    schema: dict[str, str]


def inspect_file(path: str | Path) -> InspectionResult:
    file_path = Path(path)
    df = read_table(file_path)

    return InspectionResult(
        path=file_path,
        rows=df.height,
        columns=df.width,
        schema={name: str(dtype) for name, dtype in df.schema.items()},
    )
