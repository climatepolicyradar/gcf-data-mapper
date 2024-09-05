import pandas as pd
import pytest

from gcf_data_mapper.enums.document import (
    RequiredDocumentColumns,
    RequiredFamilyDocumentColumns,
)
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
                RequiredFamilyDocumentColumns.APPROVED_REF.value: None,
            },
            "Skipping row with missing required family columns: None",
        ),
        (
            {
                RequiredFamilyDocumentColumns.APPROVED_REF.value: None,
                RequiredFamilyDocumentColumns.PROJECTS_ID.value: None,
            },
            "Skipping row with missing required family columns: None",
        ),
        (
            {
                RequiredFamilyDocumentColumns.APPROVED_REF.value: "ref123",
                RequiredFamilyDocumentColumns.PROJECTS_ID.value: "proj123",
                RequiredDocumentColumns.ID.value: None,
                RequiredDocumentColumns.TITLE.value: None,
                RequiredDocumentColumns.TYPE.value: None,
                RequiredDocumentColumns.SOURCE_URL.value: None,
            },
            "Skipping row with missing required document columns: None",
        ),
        (
            {
                RequiredFamilyDocumentColumns.APPROVED_REF.value: "ref123",
                RequiredFamilyDocumentColumns.PROJECTS_ID.value: "proj123",
                RequiredDocumentColumns.ID.value: "123",
                RequiredDocumentColumns.TITLE.value: "title123",
                RequiredDocumentColumns.TYPE.value: None,
                RequiredDocumentColumns.SOURCE_URL.value: None,
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
