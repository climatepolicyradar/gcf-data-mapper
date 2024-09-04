import pandas as pd
import pytest

from gcf_data_mapper.enums.event import Events
from gcf_data_mapper.parsers.event import check_event_dates


@pytest.fixture
def mock_row():
    return pd.Series(
        {
            Events.APPROVED.column_name: "2023-01-01",
            Events.UNDER_IMPLEMENTATION.column_name: None,
            Events.COMPLETED.column_name: "2023-12-31",
        }
    )


def test_check_event_dates_returns_correct_flags(mock_row):
    result = check_event_dates(mock_row)
    assert result[Events.APPROVED.name] is True
    assert result[Events.UNDER_IMPLEMENTATION.name] is False
    assert result[Events.COMPLETED.name] is True


def test_check_event_dates_returns_false_for_missing_columns():
    row = pd.Series(
        {
            Events.APPROVED.column_name: None,
            Events.UNDER_IMPLEMENTATION.column_name: None,
            Events.COMPLETED.column_name: None,
        }
    )
    result = check_event_dates(row)
    assert all(value is False for value in result.values())


def test_check_event_dates_returns_false_for_all_na():
    row = pd.Series(
        {
            Events.APPROVED.column_name: None,
            Events.UNDER_IMPLEMENTATION.column_name: None,
            Events.COMPLETED.column_name: None,
        }
    )
    result = check_event_dates(row)
    assert all(value is False for value in result.values())
