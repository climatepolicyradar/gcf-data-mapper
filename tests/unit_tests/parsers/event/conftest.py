import pandas as pd
import pytest


@pytest.fixture(
    params=[
        {
            "col1": ["record1"],
        },
        {
            "ApprovedRef": ["some_ref"],
        },
        {
            "ApprovedRef": ["some_ref"],
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
            "ApprovedRef": ["some_ref"],
            "StartDate": ["some_start"],
            "DateCompletion": ["some_end"],
        }
    )
