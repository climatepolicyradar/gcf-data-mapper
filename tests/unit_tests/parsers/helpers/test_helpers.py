from typing import Type

import pandas as pd
import pytest

from gcf_data_mapper.parsers.helpers import (
    check_row_for_columns_with_empty_values,
    check_row_for_missing_columns,
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


@pytest.mark.parametrize(
    ("test_data_series,required_columns,error,error_msg"),
    [
        (
            pd.Series({"Fruit": "Apple", "Plant": "Rose", "Tree": "Oak"}),
            ["Colour", "Age"],
            AttributeError,
            "The data series is missing these required columns: Colour, Age",
        )
    ],
)
def test_raises_error_for_missing_columns_in_a_given_row(
    test_data_series: pd.Series,
    required_columns: list[str],
    error: Type[Exception],
    error_msg: str,
):
    with pytest.raises(error) as e:
        check_row_for_missing_columns(test_data_series, required_columns)
    assert error_msg in str(e.value)


@pytest.mark.parametrize(
    ("test_ds,required_columns,error,error_msg"),
    [
        (
            pd.Series({"Fruit": pd.NA, "Plant": pd.NA, "Tree": "Oak"}),
            ["Fruit", "Plant"],
            ValueError,
            "This row has columns with empty values",
        )
    ],
)
def test_raises_error_for_columns_with_empty_values_in_a_given_row(
    test_ds: pd.Series,
    required_columns: list[str],
    error: Type[Exception],
    error_msg: str,
):
    with pytest.raises(error) as e:
        check_row_for_columns_with_empty_values(test_ds, required_columns)
    assert error_msg in str(e.value)
