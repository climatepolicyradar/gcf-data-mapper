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
            "DateImplementationStart": [None, "2023-06-01"],
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
            "DateImplementationStart": [None, None],
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
            "DateImplementationStart": [None, "  2023-06-01"],
        }
    )
    result = event(projects_data, debug=False)
    assert len(result) == 3


def test_handles_data_with_leading_and_trailing_whitespace():
    mock_projects_data = pd.DataFrame(
        {
            "ApprovalDate": [" 2023-01-01 ", None],
            "StartDate": [None, "  2023-06-01"],
            "DateCompletion": ["2023-12-31  ", None],
            "ApprovedRef": ["  FP123  ", " FP124 "],
            "ProjectsID": [" PID456 ", "  PID457  "],
            "DateImplementationStart": [None, "  2023-06-01"],
        }
    )

    expected_mapped_events = [
        {
            "date": "2023-01-01",
            "event_title": "Project Approved",
            "event_type_value": "Project Approved",
            "import_id": "GCF.event.FP123_PID456.n0000",
            "family_import_id": "GCF.family.FP123.PID456",
        },
        {
            "date": "2023-12-31",
            "event_title": "Project Completed",
            "event_type_value": "Project Completed",
            "family_import_id": "GCF.family.FP123.PID456",
            "import_id": "GCF.event.FP123_PID456.n0001",
        },
        {
            "date": "2023-06-01",
            "event_title": "Under Implementation",
            "event_type_value": "Under Implementation",
            "family_import_id": "GCF.family.FP124.PID457",
            "import_id": "GCF.event.FP124_PID457.n0000",
        },
    ]

    assert expected_mapped_events == event(mock_projects_data, False)
