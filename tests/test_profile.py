from dishwasher.profile import profile_file


def test_profile_csv(tmp_path):
    path = tmp_path / "people.csv"
    path.write_text(
        "name,age,city\nAda,36,London\nLinus,55,\nAda,36,London\n",
        encoding="utf-8",
    )

    result = profile_file(path)

    assert result.rows == 3
    assert result.columns == 3

    profiles = {column.name: column for column in result.column_profiles}

    assert profiles["name"].dtype == "String"
    assert profiles["name"].null_count == 0
    assert profiles["name"].unique_count == 2

    assert profiles["city"].null_count == 1
    assert profiles["city"].unique_count == 2
