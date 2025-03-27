import pandas as pd
import pytest

from gcf_data_mapper.enums.family import FamilyColumnsNames, FamilyNestedColumnNames


@pytest.fixture()
def mock_family_doc_df():
    yield pd.DataFrame(
        [
            {
                "ProjectsID": 12660,
                "ApprovedRef": "FP003",
                "ProjectName": "Enhancing resilience of coastal ecosystems and communities",
                "Theme": "Adaptation",
                "Sector": "Environment",
                "ProjectURL": "https://www.climateaction.fund/project/FP003",
                "Summary": "The Summary of the Project",
                "Countries": [
                    {
                        "CountryName": "Bangladesh",
                        "ISO3": "BGD",
                        "Region": "Asia",
                    },
                ],
                "Entities": [
                    {
                        "Name": "Green Innovations",
                    }
                ],
                "Funding": [
                    {
                        "Source": "GCF",
                        "Budget": 9200000,
                        "BudgetUSDeq": 9200000,
                    },
                    {
                        "ProjectBudgetID": 412,
                        "Source": "Co-Financing",
                        "Budget": 620000,
                        "BudgetUSDeq": 620000,
                    },
                ],
                "ResultAreas": [
                    {
                        "Area": "Coastal protection and restoration",
                        "Type": "Adaptation",
                        "Value": "100%",
                    },
                ],
                "ApprovalDate": "2016-06-30T00:00:00.000Z",
                "StartDate": "2024-06-28T00:00:00.000Z",
                "DateCompletion": None,
                "Status": "Under Implementation",
                "DateImplementationStart": None,
            }
        ]
    )


@pytest.fixture()
def mock_family_row_ds():
    yield pd.Series(
        {
            "ProjectsID": 1,
            "ApprovedRef": "FP004",
            "ProjectName": "Enhancing resilience of marine ecosystems",
            "Theme": "Adaptation",
            "Sector": "Private",
            "ProjectURL": "https://www.climateaction.fund/project/FP004",
            "Summary": "The Summary of the Project",
            "Countries": [
                {
                    "CountryName": "Haiti",
                    "ISO3": "HTI",
                    "Region": "Latin America and the Caribbean",
                },
            ],
            "Entities": [
                {
                    "Name": "Climate Action Innovations",
                }
            ],
            "Funding": [
                {
                    "Source": "GCF",
                    "Budget": 82000,
                    "BudgetUSDeq": 82000,
                },
                {
                    "ProjectBudgetID": 412,
                    "Source": "Co-Financing",
                    "Budget": 620000,
                    "BudgetUSDeq": 620000,
                },
            ],
            "ResultAreas": [
                {
                    "Area": "The Area for the Result Area",
                    "Type": "The Type for the Result Area",
                    "Value": "100%",
                },
            ],
            "ApprovalDate": "2016-06-30T00:00:00.000Z",
            "StartDate": "2024-06-28T00:00:00.000Z",
            "DateCompletion": None,
        }
    )


@pytest.fixture()
def mock_family_row_no_result_areas():
    yield pd.Series(
        {
            "ProjectsID": 2,
            "ApprovedRef": "FP004",
            "ProjectName": "Enhancing resilience of marine ecosystems",
            "Theme": "Adaptation",
            "Sector": "Private",
            "ProjectURL": "https://www.climateaction.fund/project/FP004",
            "Summary": "The Summary of the Project",
            "Countries": [
                {
                    "CountryName": "Haiti",
                    "ISO3": "HTI",
                    "Region": "Latin America and the Caribbean",
                },
            ],
            "Entities": [
                {
                    "Name": "Climate Action Innovations",
                }
            ],
            "Funding": [
                {
                    "Source": "GCF",
                    "Budget": 82000,
                    "BudgetUSDeq": 82000,
                },
                {
                    "ProjectBudgetID": 412,
                    "Source": "Co-Financing",
                    "Budget": 620000,
                    "BudgetUSDeq": 620000,
                },
            ],
            "ResultAreas": [
                {"Area": "", "Type": "", "Value": ""},
            ],
            "ApprovalDate": "2016-06-30T00:00:00.000Z",
            "StartDate": "2024-06-28T00:00:00.000Z",
            "DateCompletion": None,
        }
    )


@pytest.fixture()
def mock_family_row_no_entities_no_regions():
    yield pd.Series(
        {
            "ProjectsID": 3,
            "ApprovedRef": "FP004",
            "ProjectName": "Enhancing resilience of marine ecosystems",
            "Theme": "Adaptation",
            "Sector": "Private",
            "ProjectURL": "https://www.climateaction.fund/project/FP004",
            "Summary": "The Summary of the Project",
            "Countries": [
                {"Region": ""},
            ],
            "Entities": [{"Name": ""}],
            "Funding": [
                {
                    "Source": "GCF",
                    "Budget": 82000,
                    "BudgetUSDeq": 82000,
                },
                {
                    "ProjectBudgetID": 412,
                    "Source": "Co-Financing",
                    "Budget": 620000,
                    "BudgetUSDeq": 620000,
                },
            ],
            "ResultAreas": [
                {
                    "Area": "The Area for the Result Area",
                    "Type": "The Type for the Result Area",
                    "Value": "100%",
                },
            ],
            "ApprovalDate": "2016-06-30T00:00:00.000Z",
            "StartDate": "2024-06-28T00:00:00.000Z",
            "DateCompletion": None,
        }
    )


@pytest.fixture()
def mock_family_row_with_non_int_non_float_budget_values():
    yield pd.Series(
        {
            "ProjectsID": 3,
            "ApprovedRef": "FP004",
            "ProjectName": "Enhancing resilience of marine ecosystems",
            "Theme": "Adaptation",
            "Sector": "Private",
            "ProjectURL": "https://www.climateaction.fund/project/FP004",
            "Summary": "The Summary of the Project",
            "Countries": [
                {"Region": ""},
            ],
            "Entities": [{"Name": ""}],
            "Funding": [
                {
                    "Source": "GCF",
                    "Budget": "82000",
                    "BudgetUSDeq": "82000",
                },
                {
                    "Source": "Co-Financing",
                    "Budget": "620000.20",
                    "BudgetUSDeq": "620000.50",
                },
            ],
            "ResultAreas": [
                {
                    "Area": "The Area for the Result Area",
                    "Type": "The Type for the Result Area",
                    "Value": "100%",
                },
            ],
            "ApprovalDate": "2016-06-30T00:00:00.000Z",
            "StartDate": "2024-06-28T00:00:00.000Z",
            "DateCompletion": None,
        }
    )


@pytest.fixture()
def mock_family_doc_with_whitespace():
    yield pd.Series(
        {
            "ProjectsID": "  AAABBB  ",
            "ApprovedRef": " FP003 ",
            "ProjectName": "  Enhancing resilience of coastal ecosystems and communities",
            "Theme": " Adaptation ",
            "Sector": " Environment ",
            "ProjectURL": " https://www.climateaction.fund/project/FP003   ",
            "Summary": " The Summary of the Project ",
            "Countries": [
                {
                    "CountryName": " Bangladesh ",
                    "ISO3": " BGD ",
                    "Region": " Asia   ",
                },
            ],
            "Entities": [
                {
                    "Name": " Green Innovations  ",
                }
            ],
            "Funding": [
                {
                    "Source": " GCF ",
                    "Budget": 9200000,
                    "BudgetUSDeq": 9200000,
                },
                {
                    "ProjectBudgetID": 412,
                    "Source": " Co-Financing  ",
                    "Budget": 620000,
                    "BudgetUSDeq": 620000,
                },
            ],
            "ResultAreas": [
                {
                    "Area": " Coastal protection and restoration ",
                    "Type": " Adaptation  ",
                    "Value": "100%",
                },
            ],
            "ApprovalDate": " 2016-06-30T00:00:00.000Z ",
            "StartDate": " 2024-06-28T00:00:00.000Z  ",
            "DateCompletion": None,
        }
    )


@pytest.fixture()
def required_family_columns():
    required_columns = [column.value for column in FamilyColumnsNames]
    required_nested_family_columns = [
        column.value for column in FamilyNestedColumnNames
    ]

    return required_columns, required_nested_family_columns
