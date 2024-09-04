import pandas as pd
import pytest

from gcf_data_mapper.enums.document import (
    DocumentVariantNames,
    RequiredDocumentColumns,
    RequiredFamilyDocumentColumns,
)
from gcf_data_mapper.parsers.document import map_document_metadata


@pytest.fixture
def mock_row():
    return pd.Series(
        {
            RequiredFamilyDocumentColumns.APPROVED_REF.value: "ref123",
            RequiredFamilyDocumentColumns.PROJECTS_ID.value: "proj123",
            RequiredDocumentColumns.ID.value: "doc123",
            RequiredDocumentColumns.TYPE.value: "type123",
            RequiredDocumentColumns.TITLE.value: "title123",
            "Document page permalink": "link123",
        }
    )


def test_map_document_metadata_with_source_url(mock_row):
    source_url = "http://example.com"
    result = map_document_metadata(
        mock_row, DocumentVariantNames.ORIGINAL.value, source_url
    )
    assert result["source_url"] == source_url


def test_map_document_metadata_without_source_url(mock_row):
    result = map_document_metadata(mock_row, DocumentVariantNames.ORIGINAL.value)
    assert (
        "source_url" in result
        and result["source_url"] == mock_row["Document page permalink"]
    )
