import pandas as pd
import pytest

from gcf_data_mapper.enums.event import Events
from gcf_data_mapper.parsers.event import process_event


@pytest.fixture
def mock_row():
    return pd.Series(
        {
            Events.APPROVED.column_name: "2023-01-01",
            Events.UNDER_IMPLEMENTATION.column_name: None,
            Events.COMPLETED.column_name: "2023-12-31",
            "ApprovedRef": "FP123",
            "ProjectsID": "PID456",
        }
    )


def test_process_event_adds_events_to_list(mock_row):
    gcf_events = []
    event_counter = {}
    process_event(mock_row, gcf_events, event_counter, "FP123", "PID456")
    assert len(gcf_events) == 2
    assert event_counter["GCF.event.FP123.PID456"] == 2


def test_process_event_handles_no_dates():
    row = pd.Series(
        {
            Events.APPROVED.column_name: None,
            Events.UNDER_IMPLEMENTATION.column_name: None,
            Events.COMPLETED.column_name: None,
            "ApprovedRef": "FP123",
            "ProjectsID": "PID456",
        }
    )
    gcf_events = []
    event_counter = {}
    process_event(row, gcf_events, event_counter, "FP123", "PID456")
    assert len(gcf_events) == 0
    assert event_counter["GCF.event.FP123.PID456"] == 0


def test_process_event_handles_partial_dates():
    row = pd.Series(
        {
            Events.APPROVED.column_name: "2023-01-01",
            Events.UNDER_IMPLEMENTATION.column_name: "2023-06-01",
            Events.COMPLETED.column_name: None,
            "ApprovedRef": "FP123",
            "ProjectsID": "PID456",
        }
    )
    gcf_events = []
    event_counter = {}
    process_event(row, gcf_events, event_counter, "FP123", "PID456")
    assert len(gcf_events) == 2
    assert event_counter["GCF.event.FP123.PID456"] == 2


def test_process_event_raises_key_error_for_missing_columns():
    row = pd.Series({"ApprovedRef": "FP123", "ProjectsID": "PID456"})
    gcf_events = []
    event_counter = {}
    with pytest.raises(KeyError):
        process_event(row, gcf_events, event_counter, "FP123", "PID456")
