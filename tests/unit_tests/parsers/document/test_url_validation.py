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


@pytest.mark.parametrize(
    "urls, expected",
    [
        (["http://example.com", ""], True),
        (["http://example.com", "http://example.org"], False),
    ],
)
def test_contains_empty_urls(urls, expected):
    assert contains_empty_urls(urls) == expected


@pytest.mark.parametrize(
    "urls, expected",
    [
        (["http://example.com/valid", "http://example.com/also_valid"], False),
        (["http://example.com/valid", "http://example.com/invalid path"], True),
    ],
)
def test_contains_invalid_paths(urls, expected):
    assert contains_invalid_paths(urls) == expected


@pytest.mark.parametrize(
    "urls, doc_id, expected",
    [
        (["http://example.com", "http://example.org"], "doc123", True),
        (["some_url1", "some_url2"], "doc456", True),
        (["http://example.com/valid", "http://example.com/also_valid"], "doc789", True),
    ],
)
def test_url_validation_passes_with_valid_urls(urls, doc_id, expected):
    assert validate_urls(urls, doc_id) == expected


@pytest.mark.parametrize(
    "urls, doc_id, expected",
    [
        (["http://example.com", "http://example.com"], "doc123", None),
        (["http://example.com", ""], "doc456", None),
        (
            ["http://example.com/valid", "http://example.com/invalid path"],
            "doc789",
            None,
        ),
    ],
)
def test_url_validation_returns_none_when_fails(urls, doc_id, expected):
    assert validate_urls(urls, doc_id) == expected
