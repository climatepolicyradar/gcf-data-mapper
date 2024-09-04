import pandas as pd
import pytest

from gcf_data_mapper.enums.document import (
    RequiredDocumentColumns,
    RequiredFamilyDocumentColumns,
)
from gcf_data_mapper.parsers.document import document


@pytest.fixture
def mock_gcf_docs():
    return pd.DataFrame(
        {
            "FP number": ["FP123", "FP124"],
            RequiredDocumentColumns.ID.value: ["doc123", "doc124"],
            RequiredDocumentColumns.TYPE.value: ["type123", "type124"],
            RequiredDocumentColumns.TITLE.value: ["title123", "title124"],
            "Translated titles": ["title123_fr", "title124_fr"],
            "Document page permalink": ["link123", "link124"],
            "Translated files": ["file123_fr", "file124_fr"],
        }
    )


@pytest.fixture
def mock_projects_data():
    return pd.DataFrame(
        {
            RequiredFamilyDocumentColumns.APPROVED_REF.value: ["FP123", "FP124"],
            RequiredFamilyDocumentColumns.PROJECTS_ID.value: ["proj123", "proj124"],
        }
    )


def test_document_mapping_successful_with_valid_data(mock_gcf_docs, mock_projects_data):
    result = document(mock_projects_data, mock_gcf_docs, debug=False)
    assert isinstance(result, list)


def test_document_no_merge(mock_gcf_docs, mock_projects_data):
    mock_gcf_docs = mock_gcf_docs.assign(**{"FP number": ["FP125", "FP126"]})
    result = document(mock_projects_data, mock_gcf_docs, debug=False)
    assert all(doc is None for doc in result)
