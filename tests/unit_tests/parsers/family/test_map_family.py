import pandas as pd
import pytest

from gcf_data_mapper.parsers.family import family, map_family_data, process_row


@pytest.fixture
def parsed_family_data():
    return [
        {
            "category": "MCF",
            "collections": [],
            "description": "The Summary of the Project",
            "geographies": ["BGD"],
            "import_id": "GCF.family.FP003.12660",
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
            },
            "title": "Enhancing resilience of coastal ecosystems and communities",
        }
    ]


def test_returns_expected_family_data_structure(
    mock_family_doc_df: pd.DataFrame, parsed_family_data: list[dict]
):
    family_data = family(mock_family_doc_df, debug=True)
    assert family_data != []
    assert len(family_data) == len(parsed_family_data)
    assert family_data == parsed_family_data


def test_returns_expected_import_id_for_family_data(
    mock_family_row_ds: pd.Series,
):
    approved_ref = mock_family_row_ds.ApprovedRef
    projects_id = mock_family_row_ds.ProjectsID

    family_data = map_family_data(mock_family_row_ds)
    assert family_data is not None
    assert family_data["import_id"] == f"GCF.family.{approved_ref}.{projects_id}"


def test_raises_error_on_validating_row_for_missing_columns():
    test_data_frame = pd.DataFrame(
        [
            {
                "ApprovedRef": "approved_ref",
                "Entities": "Fake Entity",
                "Funding": [{"Source": "GCF"}],
                "ProjectURL": "www.fake-url.com",
                "ProjectsID": 100,
                "ResultAreas": [{"Area": "Coastal"}],
                "Summary": "Fake Summary",
                "ProjectName": "Fake Project Name",
            }
        ]
    )

    expected_error_message = "Required fields ['Countries', 'Sector', 'Theme'] not present in df columns ['ApprovedRef', 'Entities', 'Funding', 'ProjectName', 'ProjectURL', 'ProjectsID', 'ResultAreas', 'Summary']"
    with pytest.raises(AttributeError) as e:
        family(test_data_frame, debug=True)
    assert expected_error_message == str(e.value)


@pytest.mark.parametrize(
    ("test_ds,expected_return,error_message"),
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
                    "ProjectName": "Fake Project Name",
                    "ResultAreas": [{"Area": "Coastal"}],
                    "Sector": "TestSector",
                    "Summary": "Fake Summary",
                    "Theme": "TestTheme",
                }
            ),
            None,
            "🛑 Skipping row as it contains empty column values: See Project ID 100",
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
        (
            pd.Series(
                {
                    "ApprovedRef": pd.NA,
                    "Countries": pd.NA,
                    "Entities": pd.NA,
                    "Funding": [{"Source": "GCF"}],
                    "ProjectURL": "www.fake-url.com",
                    "ProjectsID": "",
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
    test_ds: pd.Series,
    expected_return,
    error_message: str,
    capsys,
    required_family_columns,
):
    projects_id = test_ds.ProjectsID

    columns, _ = required_family_columns
    family_data = process_row(test_ds, projects_id, columns)
    assert expected_return == family_data
    captured = capsys.readouterr()
    assert error_message == captured.out.strip()


def test_skips_processing_row_if_family_metadata_has_missing_data(
    mock_family_row_no_result_areas, capsys
):
    family_data = map_family_data(mock_family_row_no_result_areas)
    assert family_data is None
    captured = capsys.readouterr()
    # We have two outputs, one from map_family_metadata pointing to the missing data and the second
    # from map_family_data informing that the row is being skipped
    map_family_data_output = captured.out.strip().split("\n")
    assert (
        "🛑 Skipping row as family metadata has missing information"
        == map_family_data_output[1]
    )
