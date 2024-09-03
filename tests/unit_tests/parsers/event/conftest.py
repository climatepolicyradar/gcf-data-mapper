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
        }
    )
