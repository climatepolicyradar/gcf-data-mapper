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
            Events.UNDER_IMPLEMENTATION_SECONDARY.column_name: "2023-02-02",
        }
    )


def test_check_event_dates_returns_correct_flags(mock_row):
    result = check_event_dates(mock_row)
    assert result[Events.APPROVED.name] is True
    assert result[Events.UNDER_IMPLEMENTATION.name] is False
    assert result[Events.COMPLETED.name] is True
    assert result[Events.UNDER_IMPLEMENTATION_SECONDARY.name] is True


def test_check_event_dates_returns_correct_flag_for_under_implementation_secondary_if_under_implementation_date_present():
    mock_row = pd.Series(
        {
            Events.APPROVED.column_name: "2023-01-01",
            Events.UNDER_IMPLEMENTATION.column_name: "2023-02-02",
            Events.COMPLETED.column_name: "2023-12-31",
            Events.UNDER_IMPLEMENTATION_SECONDARY.column_name: "2023-02-02",
        }
    )
    result = check_event_dates(mock_row)
    assert result[Events.UNDER_IMPLEMENTATION.name] is True
    assert result[Events.UNDER_IMPLEMENTATION_SECONDARY.name] is False


def test_check_event_dates_returns_false_for_missing_columns():
    row = pd.Series(
        {
            Events.APPROVED.column_name: None,
            Events.UNDER_IMPLEMENTATION.column_name: None,
            Events.COMPLETED.column_name: None,
            Events.UNDER_IMPLEMENTATION_SECONDARY.column_name: None,
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
            Events.UNDER_IMPLEMENTATION_SECONDARY.column_name: None,
        }
    )
    result = check_event_dates(row)
    assert all(value is False for value in result.values())
