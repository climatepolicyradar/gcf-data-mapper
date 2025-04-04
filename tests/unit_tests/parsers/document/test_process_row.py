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


def test_handles_data_with_leading_and_trailing_whitespace(
    mock_valid_row_with_whitespace,
):

    expected_mapped_doc = [
        {
            "import_id": "GCF.document.ref123_proj123.doc123",
            "family_import_id": "GCF.family.ref123.proj123",
            "metadata": {"type": ["type123"]},
            "title": "title123",
            "source_url": "link123.pdf",
            "variant_name": "Original Language",
        }
    ]

    assert expected_mapped_doc == process_row(mock_valid_row_with_whitespace, False)


@pytest.mark.parametrize(
    ("test_ds,expected_return,error_message"),
    [
        (
            pd.Series(
                {
                    "ApprovedRef": "ref123",
                    "ProjectsID": "proj123",
                    "ID (Unique ID from our CMS for the document)": "doc123",
                    "Type": "Test type",
                    "Title": "Test title",
                    "Main file (English)": "link123.pdf",
                    "Document page permalink": "link123",
                    "Translated files": pd.NA,
                    "Translated titles": pd.NA,
                }
            ),
            [
                {
                    "import_id": "GCF.document.ref123_proj123.doc123",
                    "family_import_id": "GCF.family.ref123.proj123",
                    "metadata": {"type": ["Test type"]},
                    "title": "Test title",
                    "source_url": "link123.pdf",
                    "variant_name": "Original Language",
                }
            ],
            None,
        ),
        (
            pd.Series(
                {
                    "ApprovedRef": "ref123",
                    "ProjectsID": "proj123",
                    "ID (Unique ID from our CMS for the document)": "doc123",
                    "Type": "Test type",
                    "Title": "Test title",
                    "Main file (English)": "link123.PDF",
                    "Document page permalink": "link123",
                    "Translated files": pd.NA,
                    "Translated titles": pd.NA,
                }
            ),
            [
                {
                    "import_id": "GCF.document.ref123_proj123.doc123",
                    "family_import_id": "GCF.family.ref123.proj123",
                    "metadata": {"type": ["Test type"]},
                    "title": "Test title",
                    "source_url": "link123.PDF",
                    "variant_name": "Original Language",
                }
            ],
            None,
        ),
        (
            pd.Series(
                {
                    "ApprovedRef": "ref123",
                    "ProjectsID": "proj123",
                    "ID (Unique ID from our CMS for the document)": "doc123",
                    "Type": "Test type",
                    "Title": "Test title",
                    "Main file (English)": "link123.html",
                    "Document page permalink": "link123",
                    "Translated files": pd.NA,
                    "Translated titles": pd.NA,
                }
            ),
            [
                {
                    "import_id": "GCF.document.ref123_proj123.doc123",
                    "family_import_id": "GCF.family.ref123.proj123",
                    "metadata": {"type": ["Test type"]},
                    "title": "Test title",
                    "source_url": "link123.html",
                    "variant_name": "Original Language",
                }
            ],
            None,
        ),
        (
            pd.Series(
                {
                    "ApprovedRef": "ref123",
                    "ProjectsID": "proj123",
                    "ID (Unique ID from our CMS for the document)": "doc123",
                    "Type": "Test type",
                    "Title": "Test title",
                    "Main file (English)": "link123.HTML",
                    "Document page permalink": "link123",
                    "Translated files": pd.NA,
                    "Translated titles": pd.NA,
                }
            ),
            [
                {
                    "import_id": "GCF.document.ref123_proj123.doc123",
                    "family_import_id": "GCF.family.ref123.proj123",
                    "metadata": {"type": ["Test type"]},
                    "title": "Test title",
                    "source_url": "link123.HTML",
                    "variant_name": "Original Language",
                }
            ],
            None,
        ),
        (
            pd.Series(
                {
                    "ApprovedRef": "ref123",
                    "ProjectsID": "proj123",
                    "ID (Unique ID from our CMS for the document)": "doc123",
                    "Type": "Test type",
                    "Title": "Test title",
                    "Main file (English)": "link123.xlsx",
                    "Document page permalink": "link123",
                    "Translated files": pd.NA,
                    "Translated titles": pd.NA,
                }
            ),
            None,
            "🛑 Skipping row as [.xlsx] is not a valid file ext. Project ID: doc123",
        ),
    ],
)
def test_validates_url_has_a_supported_extension(
    test_ds: pd.Series,
    expected_return,
    error_message: str,
    capsys,
):
    document_data = process_row(test_ds, debug=False)

    assert expected_return == document_data

    if error_message:
        captured = capsys.readouterr()
        assert error_message == captured.out.strip()
