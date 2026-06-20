import pytest
from api.validators.csv_file_name_validator import CsvFileNameValidator


def test_valid_simple_name():
    CsvFileNameValidator("users.csv").validate()


def test_valid_name_with_underscore():
    CsvFileNameValidator("point_history.csv").validate()


def test_valid_name_with_hyphen():
    CsvFileNameValidator("my-data.csv").validate()


def test_valid_name_with_numbers():
    CsvFileNameValidator("data2024.csv").validate()


def test_no_extension_raises():
    with pytest.raises(ValueError, match="拡張子"):
        CsvFileNameValidator("users").validate()


def test_wrong_extension_raises():
    with pytest.raises(ValueError, match="拡張子"):
        CsvFileNameValidator("users.txt").validate()


def test_empty_table_name_raises():
    with pytest.raises(ValueError, match="空"):
        CsvFileNameValidator(".csv").validate()


def test_space_in_name_raises():
    with pytest.raises(ValueError, match="スペース"):
        CsvFileNameValidator("my file.csv").validate()


def test_japanese_chars_raises():
    with pytest.raises(ValueError, match="使用できません"):
        CsvFileNameValidator("ユーザー.csv").validate()


def test_dot_in_table_name_raises():
    with pytest.raises(ValueError, match="使用できません"):
        CsvFileNameValidator("my.file.csv").validate()
