import pandas as pd
import pytest

from gcf_data_mapper.parsers.helpers import verify_required_fields_present


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
