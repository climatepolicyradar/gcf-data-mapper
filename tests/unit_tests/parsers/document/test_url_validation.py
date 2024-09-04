import pytest

from gcf_data_mapper.parsers.document import (
    contains_duplicate_urls,
    contains_empty_urls,
    contains_invalid_paths,
    validate_urls,
)


@pytest.mark.parametrize(
    "urls, expected",
    [
        (["http://example.com", "http://example.com"], True),
        (["http://example.com", "http://example.org"], False),
    ],
)
def test_contains_duplicate_urls(urls, expected):
    assert contains_duplicate_urls(urls) == expected


def test_no_duplicates_when_urls_unique():
    assert not contains_duplicate_urls([])


@pytest.mark.parametrize(
    "urls, expected",
    [
        (["http://example.com", ""], True),
        (["http://example.com", "http://example.org"], False),
    ],
)
def test_contains_empty_urls(urls, expected):
    assert contains_empty_urls(urls) == expected


def test_no_empty_urls():
    assert not contains_empty_urls(["http://example.com", "http://example.org"])


@pytest.mark.parametrize(
    "urls, expected",
    [
        (["http://example.com/valid", "http://example.com/also_valid"], False),
        (["http://example.com/valid", "http://example.com/invalid path"], True),
    ],
)
def test_contains_invalid_paths(urls, expected):
    assert contains_invalid_paths(urls) == expected


def test_no_invalid_paths_when_urls_well_formed():
    assert not contains_invalid_paths([])


@pytest.mark.parametrize(
    "urls, doc_id, expected",
    [
        (["http://example.com", "http://example.org"], "doc123", True),
        (["http://example.com", ""], "doc123", None),
    ],
)
def test_url_validation_passes_with_valid_urls(urls, doc_id, expected):
    assert validate_urls(urls, doc_id) == expected


def test_url_validation_fails_with_duplicate_urls():
    urls = ["http://example.com", "http://example.com"]
    doc_id = "doc123"
    assert validate_urls(urls, doc_id) is None
