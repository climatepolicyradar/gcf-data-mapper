import pandas as pd
import pytest

from gcf_data_mapper.parsers.document import process_row


@pytest.mark.parametrize(
    "valid_doc_row",
    [
        "mock_valid_doc_row_with_one_translation",
        "mock_valid_doc_row_with_two_translations",
        "mock_valid_doc_row_with_many_translations",
    ],
)
def test_process_row_with_translations_success(valid_doc_row, request):
    result = process_row(request.getfixturevalue(valid_doc_row), debug=False)
    assert isinstance(result, list)


def test_process_row_with_no_translations_success(
    mock_valid_doc_row_with_no_translations,
):
    result = process_row(mock_valid_doc_row_with_no_translations, debug=False)
    assert isinstance(result, list)


@pytest.mark.parametrize(
    ("row_with_missing_cols", "expected_error_msg"),
    [
        (
            {
                "ApprovedRef": None,
            },
            "Skipping row with missing required family columns: None",
        ),
        (
            {
                "ApprovedRef": None,
                "ProjectsID": None,
            },
            "Skipping row with missing required family columns: None",
        ),
        (
            {
                "ApprovedRef": "ref123",
                "ProjectsID": "proj123",
                "ID (Unique ID from our CMS for the document)": None,
                "Title": None,
                "Type": None,
                "Document page permalink": None,
            },
            "Skipping row with missing required document columns: None",
        ),
        (
            {
                "ApprovedRef": "ref123",
                "ProjectsID": "proj123",
                "ID (Unique ID from our CMS for the document)": "123",
                "Title": "title123",
                "Type": None,
                "Document page permalink": None,
            },
            "Skipping row with missing required document columns: 123",
        ),
    ],
)
def test_process_row_returns_none_with_na_in_required_columns(
    row_with_missing_cols, expected_error_msg, capsys
):
    row = pd.Series(row_with_missing_cols)
    assert process_row(row, debug=False) is None
    captured = capsys.readouterr()
    assert expected_error_msg in captured.out
