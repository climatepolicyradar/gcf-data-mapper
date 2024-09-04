import pandas as pd
import pytest

from gcf_data_mapper.parsers.event import event


@pytest.fixture
def mock_projects_data():
    return pd.DataFrame(
        {
            "ApprovalDate": ["2023-01-01", None],
            "StartDate": [None, "2023-06-01"],
            "DateCompletion": ["2023-12-31", None],
            "ApprovedRef": ["FP123", "FP124"],
            "ProjectsID": ["PID456", "PID457"],
        }
    )


def test_event_returns_correct_number_of_events(mock_projects_data):
    result = event(mock_projects_data, debug=False)
    assert len(result) == 3


def test_event_raises_attribute_error_for_missing_fields():
    projects_data = pd.DataFrame({})
    with pytest.raises(AttributeError):
        event(projects_data, debug=False)


def test_event_logs_debug_message(mock_projects_data, capsys):
    result = event(mock_projects_data, debug=True)
    captured = capsys.readouterr()
    assert "📝 Wrangling GCF event data." in captured.out
    assert len(result) == 3


def test_event_returns_empty_list_for_no_valid_dates():
    projects_data = pd.DataFrame(
        {
            "ApprovalDate": [None, None],
            "StartDate": [None, None],
            "DateCompletion": [None, None],
            "ApprovedRef": ["FP123", "FP124"],
            "ProjectsID": ["PID456", "PID457"],
        }
    )
    result = event(projects_data, debug=False)
    assert len(result) == 0


def test_event_handles_partial_valid_dates():
    projects_data = pd.DataFrame(
        {
            "ApprovalDate": ["2023-01-01", None],
            "StartDate": [None, "2023-06-01"],
            "DateCompletion": [None, "2023-12-31"],
            "ApprovedRef": ["FP123", "FP124"],
            "ProjectsID": ["PID456", "PID457"],
        }
    )
    result = event(projects_data, debug=False)
    assert len(result) == 3
