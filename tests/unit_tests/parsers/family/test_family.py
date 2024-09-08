import pandas as pd
import pytest

from gcf_data_mapper.parsers.family import family, get_budgets, process_row


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


def test_returns_expected_family_data_structure(
    test_family_doc_df: pd.DataFrame, parsed_family_data: list[dict]
):
    family_data = family(test_family_doc_df, debug=True)
    assert family_data != []
    assert len(family_data) == len(parsed_family_data)
    assert family_data == parsed_family_data


def test_raises_error_on_validating_row_for_missing_columns():
    test_data_frame = pd.DataFrame(
        [
            {
                "Funding": [{"Source": "GCF"}],
                "ProjectURL": "www.fake-url.com",
                "ProjectsID": 100,
                "ResultAreas": [{"Area": "Coastal"}],
                "Sector": "TestSector",
                "Theme": "TestTheme",
            }
        ]
    )

    expected_error_message = "The data series at id 100 is missing these required columns: ApprovedRef, Countries, Entities"

    with pytest.raises(AttributeError) as e:
        family(test_data_frame, debug=True)
    assert expected_error_message == str(e.value)


@pytest.mark.parametrize(
    ("funding_list, source, expected_value"),
    [
        (
            [
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
            ],
            "GCF",
            [2000],
        ),
        (
            [
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
            ],
            "Co-Financing",
            [2000, 4000],
        ),
        (
            [
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
            ],
            "GCF",
            [0],
        ),
    ],
)
def test_returns_expected_value_when_parsing_budget_data(
    funding_list: list[dict], source: str, expected_value: list[int]
):
    budgets = get_budgets(funding_list, source)
    assert budgets == expected_value


def test_returns_empty_array_when_parsing_empty_data_frame():
    empty_data_frame = pd.DataFrame([])
    family_docs = family(empty_data_frame, debug=True)
    assert family_docs == []


@pytest.mark.parametrize(
    ("test_ds,return_value,error_message"),
    [
        (
            pd.Series(
                {
                    "ApprovedRef": pd.NA,
                    "Countries": pd.NA,
                    "Entities": pd.NA,
                    "Funding": [{"Source": "GCF"}],
                    "ProjectURL": "www.fake-url.com",
                    "ProjectsID": 100,
                    "ResultAreas": [{"Area": "Coastal"}],
                    "Sector": "TestSector",
                    "Theme": "TestTheme",
                }
            ),
            None,
            "🛑 Skipping row as it contains empty column values: See Project 100",
        ),
        (
            pd.Series(
                {
                    "ApprovedRef": pd.NA,
                    "Countries": pd.NA,
                    "Entities": pd.NA,
                    "Funding": [{"Source": "GCF"}],
                    "ProjectURL": "www.fake-url.com",
                    "ProjectsID": pd.NA,
                    "ResultAreas": [{"Area": "Coastal"}],
                    "Sector": "TestSector",
                    "Theme": "TestTheme",
                }
            ),
            None,
            "🛑 Skipping row as it does not contain a project id",
        ),
    ],
)
def test_skips_processing_row_if_row_contains_empty_values(
    test_ds, return_value, error_message, capsys
):
    return_value = process_row(test_ds)
    assert return_value is None
    captured = capsys.readouterr()
    assert error_message == captured.out.strip()
