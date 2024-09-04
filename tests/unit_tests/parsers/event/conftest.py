import pandas as pd
import pytest


@pytest.fixture(
    params=[
        {
            "col1": ["record1"],
        },
        {
            "ApprovalDate": ["some_approval"],
        },
        {
            "ApprovalDate": ["some_ref"],
            "StartDate": ["some_start"],
        },
    ]
)
def required_cols_missing(request):
    yield pd.DataFrame(request.param)


@pytest.fixture()
def valid_data():
    yield pd.DataFrame(
        {
            "ApprovalDate": ["some_approval"],
            "StartDate": ["some_start"],
            "DateCompletion": ["some_end"],
            "ApprovedRef": ["an_approved_ref"],
            "ProjectsID": ["a_project_id"],
        }
    )


@pytest.fixture
def mock_row():
    return pd.Series(
        {
            "ApprovalDate": "2023-01-01",
            "StartDate": None,
            "DateCompletion": "2023-12-31",
            "ApprovedRef": "FP123",
            "ProjectsID": "PID456",
        }
    )
