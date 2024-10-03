import pandas as pd
import pytest


@pytest.fixture(
    params=[
        {
            "ApprovedRef": "ref123",
            "ProjectsID": "proj123",
            "ID (Unique ID from our CMS for the document)": "doc123",
            "Type": "type123",
            "Title": "title123",
            "Main file (English)": "link123.pdf",
            "Document page permalink": "link123",
            "Translated files": "http://example.com",
            "Translated titles": None,
        },
        {
            "ApprovedRef": "ref123",
            "ProjectsID": "proj123",
            "ID (Unique ID from our CMS for the document)": "doc123",
            "Type": "type123",
            "Title": "title123",
            "Main file (English)": "link123.pdf",
            "Document page permalink": "link123",
            "Translated titles": None,
        },
    ]
)
def mock_valid_doc_row_with_no_translations(request):
    return pd.Series(request.param)


@pytest.fixture
def mock_valid_doc_row_with_one_translation():
    return pd.Series(
        {
            "ApprovedRef": "ref123",
            "ProjectsID": "proj123",
            "ID (Unique ID from our CMS for the document)": "doc123",
            "Type": "type123",
            "Title": "title123",
            "Main file (English)": "link123.pdf",
            "Document page permalink": "link123",
            "Translated files": "http://example.com",
            "Translated titles": "title123",
        }
    )


@pytest.fixture
def mock_valid_doc_row_with_many_translations():
    return pd.Series(
        {
            "ApprovedRef": "ref123",
            "ProjectsID": "proj123",
            "ID (Unique ID from our CMS for the document)": "doc123",
            "Type": "type123",
            "Title": "title123",
            "Main file (English)": "link123.pdf",
            "Document page permalink": "link123,link456,link789",
            "Translated files": "http://example.com|http://example.org|http://example.co.uk",
            "Translated titles": "title123|title456|title789",
        }
    )


@pytest.fixture
def mock_valid_doc_row_with_two_translations():
    return pd.Series(
        {
            "ApprovedRef": "ref123",
            "ProjectsID": "proj123",
            "ID (Unique ID from our CMS for the document)": "doc123",
            "Type": "type123",
            "Title": "title123",
            "Main file (English)": "link123.pdf",
            "Document page permalink": "link123,link456",
            "Translated files": "http://example.com|http://example.org",
            "Translated titles": "title123|title456",
        }
    )


@pytest.fixture
def mock_valid_row():
    return pd.Series(
        {
            "ApprovedRef": "ref123",
            "ProjectsID": "proj123",
            "ID (Unique ID from our CMS for the document)": "doc123",
            "Type": "type123",
            "Title": "title123",
            "Main file (English)": "link123.pdf",
            "Document page permalink": "link123",
        }
    )


@pytest.fixture
def mock_gcf_docs():
    return pd.DataFrame(
        {
            "FP number": ["FP123", "FP124"],
            "ID (Unique ID from our CMS for the document)": ["doc123", "doc124"],
            "Type": ["type123", "type124"],
            "Title": ["title123", "title124"],
            "Translated titles": ["title123_fr", "title124_fr"],
            "Document page permalink": ["link123", "link124"],
            "Main file (English)": ["link123.pdf", "link124.pdf"],
            "Translated files": ["file123_fr", "file124_fr"],
        }
    )


@pytest.fixture
def mock_projects_data():
    return pd.DataFrame(
        {
            "ApprovedRef": ["FP123", "FP124"],
            "ProjectsID": ["proj123", "proj124"],
        }
    )
