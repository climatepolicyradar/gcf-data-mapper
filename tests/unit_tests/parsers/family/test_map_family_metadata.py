import pandas as pd
import pytest

from gcf_data_mapper.parsers.family import get_budgets, map_family_metadata


@pytest.fixture()
def parsed_family_metadata():
    return {
        "approved_ref": ["FP004"],
        "implementing_agencies": ["Climate Action Innovations"],
        "project_id": [1],
        "project_url": ["https://www.climateaction.fund/project/FP004"],
        "project_value_co_financing": [620000],
        "project_value_fund_spend": [82000],
        "regions": ["Latin America and the Caribbean"],
        "result_areas": ["The Area for the Result Area"],
        "result_types": ["The Type for the Result Area"],
        "sector": ["Private"],
        "theme": ["Adaptation"],
    }


def test_returns_expected_metadata_structure(
    mock_family_row_ds: pd.Series, parsed_family_metadata: dict
):
    family_metadata = map_family_metadata(mock_family_row_ds)
    assert family_metadata is not None
    assert family_metadata == parsed_family_metadata


@pytest.mark.parametrize(
    ("mock_family_row, expected_return, output_message"),
    [
        (
            "mock_family_row_no_entities_no_regions",
            None,
            "🛑 The following lists contain empty values: Implementing Agencies, Regions. Projects ID 3",
        ),
        (
            "mock_family_row_no_result_areas",
            None,
            "🛑 The following lists contain empty values: Result Areas, Result Types. Projects ID 2",
        ),
    ],
)
def test_returns_none_if_nested_values_in_family_metadata_row_contains_empty_values(
    mock_family_row: pd.Series, expected_return, output_message: str, request, capsys
):
    family_metadata = map_family_metadata(request.getfixturevalue(mock_family_row))

    assert family_metadata == expected_return
    captured = capsys.readouterr()
    assert output_message == captured.out.strip()


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
