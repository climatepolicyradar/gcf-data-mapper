import pandas as pd
import pytest


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
