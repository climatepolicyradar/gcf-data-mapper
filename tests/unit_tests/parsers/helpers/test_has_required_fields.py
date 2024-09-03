import pandas as pd
import pytest

from gcf_data_mapper.parsers.helpers import has_required_fields


@pytest.mark.parametrize(
    ("test_df", "expected_fields"),
    [
        (
            pd.DataFrame(
                {
                    "fruits": ["apple", "banana", "cherry"],
                }
            ),
            set(["fruits", "vegetables"]),
        ),
        (
            pd.DataFrame(),
            set(["cars"]),
        ),
    ],
)
def test_returns_false_when_missing_fields(test_df, expected_fields):
    return_value = has_required_fields(test_df, expected_fields, debug=False)
    assert return_value is False


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
def test_returns_true_when_no_missing_fields(test_df, expected_fields):
    return_value = has_required_fields(test_df, expected_fields, debug=False)
    assert return_value is True
