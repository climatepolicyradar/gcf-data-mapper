import pandas as pd
import pytest

from gcf_data_mapper.parsers.family import family, get_budgets


@pytest.fixture
def parsed_family_data():
    return [
        {
            "metadata": {
                "approved_ref": ["FP003"],
                "implementing_agencies": ["Green Innovations"],
                "project_id": [12660],
                "project_url": ["https://www.climateaction.fund/project/FP003"],
                "project_value_fund_spend": [9200000],
                "project_value_co_financing": [620000],
                "regions": ["Asia"],
                "result_areas": ["Coastal protection and restoration"],
                "result_types": ["Adaptation"],
                "sector": ["Environment"],
                "theme": ["Adaptation"],
            }
        }
    ]


def test_returns_expected_family_data_structure(test_family_doc_df, parsed_family_data):
    family_data = family(test_family_doc_df, debug=True)
    assert family_data != []
    assert family_data == parsed_family_data


@pytest.mark.parametrize(
    ("test_df,error,error_msg"),
    [
        (
            pd.DataFrame(
                [
                    {
                        "Funding": "",
                        "ProjectURL": "",
                        "ProjectsID": "",
                        "ResultAreas": "",
                        "Sector": "",
                        "Theme": "",
                    }
                ]
            ),
            AttributeError,
            "The data series is missing these required columns: ApprovedRef, Countries, Entities",
        ),
        (
            pd.DataFrame(
                [
                    {
                        "ApprovedRef": None,
                        "Countries": [{"Region": "Asia"}],
                        "Entities": [{"Name": "Innovation"}],
                        "Funding": [{"Source": "GCF"}],
                        "ProjectURL": "www.fake-url.com",
                        "ProjectsID": "ABC",
                        "ResultAreas": [{"Area": "Coastal"}],
                        "Sector": "TestSector",
                        "Theme": "TestTheme",
                    }
                ]
            ),
            ValueError,
            "This row has columns with empty values",
        ),
    ],
)
def test_raises_error_on_validating_row(test_df, error, error_msg):
    with pytest.raises(error) as e:
        family(test_df, debug=True)
    assert error_msg in str(e.value)


@pytest.mark.parametrize(
    ("test_data_series, source, expected_value"),
    [
        (
            pd.Series(
                {
                    "Funding": [
                        {
                            "Source": "GCF",
                            "Budget": 1000,
                            "BudgetUSDeq": 2000,
                        },
                        {
                            "Source": "Co-Financing",
                            "Budget": 1000,
                            "BudgetUSDeq": 2000,
                        },
                    ]
                }
            ),
            "GCF",
            [2000],
        ),
        (
            pd.Series(
                {
                    "Funding": [
                        {
                            "Source": "GCF",
                            "Budget": 1000,
                            "BudgetUSDeq": 2000,
                        },
                        {
                            "Source": "Co-Financing",
                            "Budget": 1000,
                            "BudgetUSDeq": 2000,
                        },
                        {
                            "Source": "Co-Financing",
                            "Budget": 2000,
                            "BudgetUSDeq": 4000,
                        },
                    ]
                }
            ),
            "Co-Financing",
            [2000, 4000],
        ),
        (
            pd.Series(
                {
                    "Funding": [
                        {
                            "Source": "Co-Financing",
                            "Budget": 1000,
                            "BudgetUSDeq": 2000,
                        },
                        {
                            "Source": "Co-Financing",
                            "Budget": 2000,
                            "BudgetUSDeq": 4000,
                        },
                    ]
                }
            ),
            "GCF",
            [0],
        ),
    ],
)
def test_returns_expected_value_when_parsing_budget_data(
    test_data_series, source, expected_value
):
    budgets = get_budgets(test_data_series, source)
    assert budgets == expected_value


def test_returns_empty_array_when_parsing_empty_data_frame():
    empty_data_frame = pd.DataFrame([])
    family_docs = family(empty_data_frame, debug=True)

    assert family_docs == []


@pytest.mark.parametrize(
    ("test_df,error,error_msg"),
    [
        (
            pd.DataFrame(
                [
                    {
                        "ApprovedRef": "Test Approved Ref",
                        "Countries": [{"Region": "Asia"}],
                        "Entities": [{"Name": "Innovation"}],
                        "Funding": [{"BudgetUSDeq": 2000}],
                        "ProjectURL": "www.fake-url.com",
                        "ProjectsID": "Test Project ID",
                        "ResultAreas": [{"Area": "Coastal"}],
                        "Sector": "TestSector",
                        "Theme": "TestTheme",
                    }
                ]
            ),
            KeyError,
            "key: 'Source' does not exist on this dict",
        ),
        (
            pd.DataFrame(
                [
                    {
                        "ApprovedRef": "Test Approved Ref",
                        "Countries": [{"Region": "Asia"}],
                        "Entities": [{"Name": "Innovation"}],
                        "Funding": [
                            {
                                "Source": None,
                                "Budget": 2000,
                                "BudgetUSDeq": 4000,
                            },
                        ],
                        "ProjectURL": "www.fake-url.com",
                        "ProjectsID": "Test Project ID",
                        "ResultAreas": [{"Area": "Coastal"}],
                        "Sector": "TestSector",
                        "Theme": "TestTheme",
                    }
                ]
            ),
            ValueError,
            "Key 'Source' exists, but the value is empty",
        ),
    ],
)
def test_raises_error_on_validating_nested_objects_for_data(test_df, error, error_msg):
    with pytest.raises(error) as e:
        family(test_df, debug=True)
    assert error_msg in str(e.value)
