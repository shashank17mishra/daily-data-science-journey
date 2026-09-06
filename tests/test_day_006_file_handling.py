import pytest
from learning.python.day_006_file_handling import write_data_to_csv, read_data_from_csv

def test_csv_read_write(tmp_path):
    csv_file = tmp_path / "test_data.csv"
    sample_data = [
        {"id": "1", "name": "Alice", "score": "95"},
        {"id": "2", "name": "Bob", "score": "88"}
    ]
    write_data_to_csv(csv_file, sample_data)
    assert csv_file.exists()

    read_records = read_data_from_csv(csv_file)
    assert len(read_records) == 2
    assert read_records[0]["name"] == "Alice"
    assert read_records[1]["score"] == "88"
