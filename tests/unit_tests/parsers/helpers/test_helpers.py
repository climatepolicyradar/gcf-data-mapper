import pandas as pd
import pytest

from gcf_data_mapper.parsers.helpers import (
    arrays_contain_empty_values,
    check_row_for_missing_columns,
    row_contains_columns_with_empty_values,
    verify_required_fields_present,
)


@pytest.mark.parametrize(
    ("test_df", "expected_fields", "expected_error"),
    [
        (
            pd.DataFrame(
                {
                    "fruits": ["apple", "banana", "cherry"],
                }
            ),
            set(["fruits", "vegetables"]),
            "Required fields '{'vegetables'}' not present in df columns '{'fruits'}'",
        ),
        (
            pd.DataFrame(),
            set(["cars"]),
            "Required fields '{'cars'}' not present in df columns '{}'",
        ),
    ],
)
def test_returns_false_when_missing_fields(
    test_df: pd.DataFrame, expected_fields: set[str], expected_error: str
):
    with pytest.raises(AttributeError) as e:
        verify_required_fields_present(test_df, expected_fields)
    assert str(e.value) == expected_error


@pytest.mark.parametrize(
    ("test_df", "expected_fields"),
    [
        (
            pd.DataFrame(
                {
                    "fruits": ["date", "elderberry", "fig"],
                    "vegetables": ["asparagus", "beetroot", "carrot"],
                }
            ),
            set(["fruits", "vegetables"]),
        ),
        (
            pd.DataFrame(
                {
                    "cars": ["Ford", "Renault", "Audi"],
                }
            ),
            set(["cars"]),
        ),
    ],
)
def test_returns_true_when_no_missing_fields(
    test_df: pd.DataFrame, expected_fields: set[str]
):
    return_value = verify_required_fields_present(test_df, expected_fields)
    assert return_value is True


def test_raises_error_for_missing_columns_in_a_given_row():
    test_data_series = pd.Series({"Fruit": "Apple", "Plant": "Rose", "Tree": "Oak"})
    test_id_identifier = "P001"
    required_columns = ["Colour", "Age"]
    expected_error_message = (
        "The data series at id P001 is missing these required columns: Age, Colour"
    )

    with pytest.raises(AttributeError) as e:
        check_row_for_missing_columns(
            test_data_series, required_columns, test_id_identifier
        )
    assert str(e.value) == expected_error_message


@pytest.mark.parametrize(
    ("test_ds,required_columns,expected_return"),
    [
        (
            pd.Series({"Fruit": pd.NA, "Plant": pd.NA, "Tree": "Oak"}),
            ["Fruit", "Plant"],
            True,
        ),
        (
            pd.Series({"Fruit": "Apple", "Plant": "Mint", "Tree": "Rosemary"}),
            ["Fruit", "Plant"],
            False,
        ),
    ],
)
def test_checks_if_there_are_columns_with_empty_values_in_a_given_row(
    test_ds: pd.Series, required_columns: list[str], expected_return: bool
):
    result = row_contains_columns_with_empty_values(test_ds, required_columns)
    assert result == expected_return


@pytest.mark.parametrize(
    "list_values, project_id, expected_return",
    [
        (
            [
                ("Fruits", ["Apple", "Mango"]),
                ("Plants", ["Rosemary", "Mint"]),
                ("Trees", ["Oak", "Sycamore"]),
            ],
            "P001",
            False,  # Function should return False when no empty values
        ),
        (
            [
                ("Fruits", ["Apple", "Mango"]),
                ("Plants", ["", ""]),
                ("Trees", ["Oak", "Sycamore"]),
            ],
            "P002",
            True,  # Function should return True when there are empty values
        ),
        (
            [
                ("Fruits", ["Apple", "Mango"]),
                ("Plants", ["", ""]),
                ("Trees", [""]),
            ],
            "P003",
            True,
        ),
    ],
)
def test_check_arrays_for_empty_values(
    list_values: list, project_id: str, expected_return: bool
):
    result = arrays_contain_empty_values(list_values, project_id)
    assert result == expected_return
    assert type(result) is bool


@pytest.mark.parametrize(
    "list_values, project_id, expected_output",
    [
        (
            [
                ("Fruits", ["Apple", "Mango"]),
                ("Plants", ["Rosemary", "Mint"]),
                ("Trees", ["Oak", "Sycamore"]),
            ],
            "P001",
            "",  # If the array does not contain any empty values we don't expect an output
        ),
        (
            [
                ("Fruits", ["Apple", "Mango"]),
                ("Plants", ["", ""]),
                ("Trees", ["Oak", "Sycamore"]),
            ],
            "P002",
            "🛑 The following lists contain empty values: Plants. ID: P002",
        ),
    ],
)
def test_check_arrays_for_empty_values_outputs_msg_to_the_cli(
    list_values: list, project_id: str, expected_output: str, capsys
):
    arrays_contain_empty_values(list_values, project_id)
    captured = capsys.readouterr()
    assert expected_output == captured.out.strip()
