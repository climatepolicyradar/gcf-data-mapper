import pandas as pd
import pytest

from gcf_data_mapper.enums.event import Event
from gcf_data_mapper.parsers.event import append_event


@pytest.fixture
def mock_event():
    return Event(1, "Approved", "ApprovalDate")


@pytest.fixture
def mock_row():
    return pd.Series({"ApprovalDate": "2023-01-01"})


def test_append_event_adds_event_to_list(mock_event, mock_row):
    gcf_events = []
    append_event(gcf_events, mock_event, mock_row, "FP123", "PID456", 1)
    assert len(gcf_events) == 1
    assert gcf_events[0]["import_id"] == "GCF.event.FP123_PID456.n0001"


def test_append_event_raises_key_error_for_missing_column(mock_event):
    gcf_events = []
    row = pd.Series({"StartDate": "2023-01-01"})
    with pytest.raises(KeyError):
        append_event(gcf_events, mock_event, row, "FP123", "PID456", 1)


def test_append_event_handles_none_date(mock_event):
    gcf_events = []
    row = pd.Series({"ApprovalDate": None})
    append_event(gcf_events, mock_event, row, "FP123", "PID456", 1)
    assert len(gcf_events) == 1
    assert gcf_events[0]["date"] is None
