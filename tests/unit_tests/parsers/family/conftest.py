import pandas as pd
import pytest

from gcf_data_mapper.enums.family import FamilyColumnsNames, FamilyNestedColumnNames


@pytest.fixture()
def test_family_doc_df():
    yield pd.DataFrame(
        [
            {
                "ProjectsID": 12660,
                "ApprovedRef": "FP003",
                "ProjectName": "Enhancing resilience of coastal ecosystems and communities",
                "Theme": "Adaptation",
                "Sector": "Environment",
                "ProjectURL": "https://www.climateaction.fund/project/FP003",
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
                    },
                ],
            }
        ]
    )


@pytest.fixture()
def required_family_columns():
    required_columns = [column.value for column in FamilyColumnsNames]
    required_nested_family_columns = [
        column.value for column in FamilyNestedColumnNames
    ]

    return required_columns, required_nested_family_columns
