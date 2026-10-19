import pandas as pd

from gcf_data_mapper.enums.document import DocumentVariantNames
from gcf_data_mapper.parsers.document import map_document_metadata


def test_map_document_metadata_with_source_url(mock_valid_row):
    source_url = "http://example.com"
    result = map_document_metadata(
        mock_valid_row, DocumentVariantNames.ORIGINAL.value, source_url
    )
    assert result["source_url"] == source_url


def test_map_document_metadata_without_source_url(mock_valid_row):
    result = map_document_metadata(mock_valid_row, DocumentVariantNames.ORIGINAL.value)
    assert (
        "source_url" in result
        and result["source_url"] == mock_valid_row["Main file (English)"]
    )


def test_map_document_metadata_uses_old_id_for_import_id_when_present():
    test_data_with_old_id = {
        "ApprovedRef": "ref123",
        "ProjectsID": "proj123",
        "ID (New)": "doc123",
        "ID (Old)": "doc000",
        "Subtype": "type123",
        "Title": "title123",
        "Main file (English)": "link123.pdf",
        "Document page permalink": "link123",
    }

    test_row_with_old_id = pd.Series(test_data_with_old_id)

    result = map_document_metadata(
        test_row_with_old_id, DocumentVariantNames.ORIGINAL.value
    )

    assert result["import_id"] == "GCF.document.ref123_proj123.doc000"


def test_map_document_metadata_uses_new_id_for_import_id_when_old_id_not_present():
    test_data_with_old_id = {
        "ApprovedRef": "ref123",
        "ProjectsID": "proj123",
        "ID (New)": "doc123",
        "ID (Old)": None,
        "Subtype": "type123",
        "Title": "title123",
        "Main file (English)": "link123.pdf",
        "Document page permalink": "link123",
    }

    test_row_with_old_id = pd.Series(test_data_with_old_id)

    result = map_document_metadata(
        test_row_with_old_id, DocumentVariantNames.ORIGINAL.value
    )

    assert result["import_id"] == "GCF.document.ref123_proj123.doc123"
