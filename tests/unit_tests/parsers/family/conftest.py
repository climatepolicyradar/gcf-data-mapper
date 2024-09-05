import pandas as pd
import pytest


@pytest.fixture()
def test_family_doc_df():
    yield pd.DataFrame(
        [
            {
                "ProjectsID": 12660,
                "ApprovedRef": "FP003",
                "BoardMeeting": "B.12",
                "ProjectName": "Enhancing resilience of coastal ecosystems and communities",
                "StartDate": None,
                "EndDate": None,
                "ApprovalDate": "2016-03-15T00:00:00.000Z",
                "DurationMonths": 36,
                "Theme": "Adaptation",
                "Sector": "Environment",
                "LifeTimeCO2": 1000000,
                "Size": "Small",
                "RiskCategory": "Category B",
                "DirectBeneficiaries": 31500,
                "IndirectBeneficiaries": 128000,
                "TotalGCFFunding": 9200000,
                "TotalCoFinancing": 620000,
                "TotalValue": 9820000,
                "ProjectURL": "https://www.climateaction.fund/project/FP003",
                "Countries": [
                    {
                        "CountryID": 200,
                        "CountryName": "Bangladesh",
                        "ISO3": "BGD",
                        "Region": "Asia",
                        "LDCs": True,
                        "SIDS": False,
                        "Financing": [
                            {
                                "Currency": "EUR",
                                "GCF": 9200000,
                                "CoFinancing": 620000,
                                "Total": 9820000,
                            }
                        ],
                    },
                ],
                "Entities": [
                    {
                        "EntityID": 12,
                        "Name": "Green Innovations",
                        "Acronym": "GI",
                        "Access": "Indirect",
                        "Type": "Regional",
                        "AccreditationDate": "2016-05-10",
                        "Sector": "Private",
                        "ESS": "Category A",
                        "FiduciaryStandards": [
                            {"FiduciaryStandard": "Advanced", "Size": "Medium"},
                            {
                                "FiduciaryStandard": "Environmental Management",
                                "Size": "Large",
                            },
                        ],
                    }
                ],
                "Disbursements": [
                    {
                        "ProjectDisbursementID": 210,
                        "AmountDisbursed": 2345000,
                        "AmountDisbursedUSDeq": 2345000,
                        "Currency": "EUR",
                        "DateEffective": "2021-06-15",
                        "Entity": "GI",
                        "CurrentExchangeRate": {
                            "ExchangeRate": 1.2,
                            "CurrencyCode": "EUR",
                            "Source": "European Central Bank",
                            "EffectiveDate": "2024-09-01",
                        },
                    },
                    {
                        "ProjectDisbursementID": 311,
                        "AmountDisbursed": 4587000,
                        "AmountDisbursedUSDeq": 4587000,
                        "Currency": "EUR",
                        "DateEffective": "2024-01-10",
                        "Entity": "GI",
                        "CurrentExchangeRate": {
                            "ExchangeRate": 1.2,
                            "CurrencyCode": "EUR",
                            "Source": "European Central Bank",
                            "EffectiveDate": "2024-09-01",
                        },
                    },
                ],
                "Funding": [
                    {
                        "ProjectBudgetID": 210,
                        "BM": "B.12",
                        "SourceID": 7,
                        "Source": "GCF",
                        "Instrument": "Loans",
                        "Budget": 9200000,
                        "BudgetUSDeq": 9200000,
                        "Currency": "EUR",
                        "CurrentExchangeRate": {
                            "ExchangeRate": 1.2,
                            "CurrencyCode": "EUR",
                            "Source": "European Central Bank",
                            "EffectiveDate": "2024-09-01",
                        },
                    },
                    {
                        "ProjectBudgetID": 412,
                        "BM": "B.12",
                        "SourceID": 8,
                        "Source": "Co-Financing",
                        "Instrument": "Grants",
                        "Budget": 620000,
                        "BudgetUSDeq": 620000,
                        "Currency": "EUR",
                        "CurrentExchangeRate": {
                            "ExchangeRate": 1.2,
                            "CurrencyCode": "EUR",
                            "Source": "European Central Bank",
                            "EffectiveDate": "2024-09-01",
                        },
                    },
                ],
                "ResultAreas": [
                    {
                        "Area": "Coastal protection and restoration",
                        "Type": "Adaptation",
                        "Value": "25.00%",
                    },
                ],
                "DateClosing": "2026-12-01T00:00:00.000Z",
                "DateCompletion": "2027-06-01T00:00:00.000Z",
            }
        ]
    )
