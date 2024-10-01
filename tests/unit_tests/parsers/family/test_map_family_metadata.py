from typing import Optional

import pandas as pd
import pytest

from gcf_data_mapper.enums.event import Events
from gcf_data_mapper.parsers.family import (
    calculate_status,
    contains_invalid_date_entries,
    get_budgets,
    map_family_metadata,
)


@pytest.fixture()
def parsed_family_metadata():
    return {
        "approved_ref": ["FP004"],
        "implementing_agency": ["Climate Action Innovations"],
        "project_id": ["1"],
        "project_url": ["https://www.climateaction.fund/project/FP004"],
        "project_value_co_financing": ["620000"],
        "project_value_fund_spend": ["82000"],
        "region": ["Latin America and the Caribbean"],
        "result_area": ["The Area for the Result Area"],
        "result_type": ["The Type for the Result Area"],
        "sector": ["Private"],
        "status": ["Under Implementation"],
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


@pytest.fixture()
def budget_input_data():
    return [
        {
            "Source": "GCF",
            "Budget": 1000,
            "BudgetUSDeq": 2000,
        },
        {
            "Source": "Co-Financing",
            "Budget": 1500,
            "BudgetUSDeq": 2700,
        },
        {
            "Source": "Co-Financing",
            "Budget": 2300,
            "BudgetUSDeq": 4100,
        },
    ]


def test_get_budgets_returns_list_of_budgets_for_funding_source(
    budget_input_data: list,
):
    gcf_source = "GCF"
    budgets = get_budgets(budget_input_data, gcf_source)
    assert budgets == ["2000"]


def test_get_budgets_returns_multiple_budgets_where_there_are_more_than_one_entries_to_a_funding_source(
    budget_input_data: list,
):
    gcf_source = "Co-Financing"
    budgets = get_budgets(budget_input_data, gcf_source)
    assert budgets is not None
    assert budgets == ["2700", "4100"]
    assert len(budgets) == 2


def test_get_budget_returns_list_of_strings(budget_input_data: list):
    gcf_source = "GCF"
    budgets = get_budgets(budget_input_data, gcf_source)
    assert budgets is not None
    assert all(isinstance(item, str) for item in budgets)


def test_get_budget_returns_list_with_zero_where_there_are_no_matching_sources(
    budget_input_data: list,
):
    source = "fake_budget_source"
    budgets = get_budgets(budget_input_data, source)
    assert budgets is not None
    assert budgets == ["0"]


def test_map_family_metadata_returns_none_if_budget_does_not_contain_valid_int_types(
    mock_family_row_with_non_int_non_float_budget_values: pd.Series,
):
    result = map_family_metadata(mock_family_row_with_non_int_non_float_budget_values)
    assert result is None


@pytest.mark.parametrize(
    ("mock_family_row, expected_status"),
    [
        (
            pd.Series(
                {
                    "ApprovalDate": "2016-06-30T00:00:00.000Z",
                    "StartDate": None,
                    "DateCompletion": None,
                }
            ),
            Events.APPROVED.type,
        ),
        (
            pd.Series(
                {
                    "ApprovalDate": "2016-06-30T00:00:00.000Z",
                    "StartDate": "2024-06-28T00:00:00.000Z",
                    "DateCompletion": None,
                }
            ),
            Events.UNDER_IMPLEMENTATION.type,
        ),
        (
            pd.Series(
                {
                    "ApprovalDate": "2016-06-30T00:00:00.000Z",
                    "StartDate": "2018-06-30T00:00:00.000Z",
                    "DateCompletion": "2022-06-30T00:00:00.000Z",
                }
            ),
            Events.COMPLETED.type,
        ),
        (
            pd.Series(
                {
                    "ApprovalDate": None,
                    "StartDate": None,
                    "DateCompletion": None,
                }
            ),
            None,
        ),
        (
            pd.Series(
                {
                    "ApprovalDate": pd.NA,
                    "StartDate": pd.NA,
                    "DateCompletion": pd.NA,
                }
            ),
            None,
        ),
        (
            pd.Series(
                {
                    "ApprovalDate": "",  # invalid date entry
                    "StartDate": "2018-06-30T00:00:00.000Z",
                    "DateCompletion": "2022-06-30T00:00:00.000Z",
                }
            ),
            None,
        ),
    ],
)
def test_returns_status(mock_family_row: pd.Series, expected_status: Optional[str]):
    status = calculate_status(mock_family_row)
    assert status == expected_status


@pytest.mark.parametrize(
    ("list_of_dates, return_value"),
    [
        (
            [
                pd.to_datetime("2016-06-30T00:00:00.000Z"),
                pd.to_datetime("2018-06-30T00:00:00.000Z"),
                pd.to_datetime("2022-06-30T00:00:00.000Z"),
            ],
            False,
        ),
        (
            [None, None, pd.to_datetime("2016-06-30T00:00:00.000Z")],
            False,
        ),
        (
            [
                pd.to_datetime("2018-06-30T00:00:00.000Z"),
                pd.to_datetime(""),
                pd.to_datetime("2022-06-30T00:00:00.000Z"),
            ],
            True,
        ),
    ],
)
def test_dates_contain_invalid_date_entries(list_of_dates: list, return_value):
    result = contains_invalid_date_entries(list_of_dates)
    assert result == return_value


@pytest.mark.parametrize(
    ("mock_row, output_message"),
    [
        (
            pd.Series(
                {
                    "ApprovalDate": pd.NA,
                    "StartDate": pd.NA,
                    "DateCompletion": pd.NA,
                }
            ),
            "🛑 Row contains invalid date entries",
        ),
        (
            pd.Series(
                {
                    "ApprovalDate": "2016-06-30T00:00:00.000Z",
                    "StartDate": "2018-06-30T00:00:00.000Z",
                    "DateCompletion": "",
                }
            ),
            "🛑 Row contains invalid date entries",
        ),
        (
            pd.Series(
                {
                    "ApprovalDate": None,
                    "StartDate": None,
                    "DateCompletion": None,
                }
            ),
            "🛑 Row missing event date information to calculate status",
        ),
    ],
)
def test_skips_processing_row_if_calculate_status_returns_none(
    mock_row: pd.Series, output_message: str, capsys
):
    return_value = map_family_metadata(mock_row)
    assert return_value is None
    captured = capsys.readouterr()
    assert output_message == captured.out.strip()


def test_all_metadata_values_are_list_of_strings(mock_family_row_ds: pd.Series):
    family_metadata = map_family_metadata(mock_family_row_ds)
    assert family_metadata is not None

    for value in family_metadata.values():
        assert isinstance(value, list)
        assert all(isinstance(item, str) for item in value)
