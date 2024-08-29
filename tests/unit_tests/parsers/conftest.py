import pandas as pd
import pytest


@pytest.fixture()
def test_df():
    yield pd.DataFrame(
        {
            "col1": ["record1"],
        }
    )
