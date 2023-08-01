"""Test of some useful functions"""

from src.database.configuration import convert_csv_to_dict


def test_correct_csv_to_dict_conversion(shared_datadir):
    """Test the correct parsing of a csv to a dict"""

    csv_dict = convert_csv_to_dict(shared_datadir / "csv" / "test_csv.csv", ",")
    assert csv_dict == [
        {"Author": "Yogi Berra", "Quote": "You can observe a lot just by watching."}
    ]
