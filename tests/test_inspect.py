from dishwasher.inspect import inspect_file


def test_inspect_csv(tmp_path):
    path = tmp_path / "people.csv"
    path.write_text("name,age\nAda,36\nLinus,55\n", encoding="utf-8")

    result = inspect_file(path)

    assert result.rows == 2
    assert result.columns == 2
    assert result.schema == {"name": "String", "age": "Int64"}
