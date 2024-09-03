from enum import Enum
from typing import Any, Optional
from urllib.parse import urlparse

import click
import pandas as pd


class DocumentColumns(Enum):
    SOURCE_URL = "Document page permalink"
    TITLE = "Title"
    TRANSLATED_FILES = "Translated files"
    TRANSLATED_TITLES = "Translated titles"
    TYPE = "Type"


def contains_duplicate_urls(urls: list[str]) -> bool:
    """
    Checks a list of urls for any duplicate entries

    param: list[str] urls: A list of urls
    return bool: Returns true if duplicate urls are present
    """

    # Convert all URLs to lowercase for case-insensitive comparison
    lowercase_urls = [url.lower() for url in urls]
    return len(lowercase_urls) != len(set(lowercase_urls))


def contains_empty_urls(urls: list[str]) -> bool:
    """
    Checks a list of urls for any empty entries

    param: list[str] urls: a list of urls
    return bool: Returns true if empty urls are present, or false if not
    """
    for url in urls:
        if not url.strip():
            return True
    return False


def contains_invalid_paths(urls: list[str]) -> bool:
    """
    Checks a list of urls for any malformed entries

    param: list[str] urls: A list of urls
    return bool: Returns true if malformed urls are present, or false if not
    """
    for url in urls:
        parsed_url = urlparse(url)
        path = parsed_url.path
        # Reserved and unreserved characters per RFC 3986
        reserved_and_unreserved_characters = ":/?#[]@!$&'()*+,;=-_.~"
        if any(
            not (c.isalnum() or c in reserved_and_unreserved_characters) for c in path
        ):
            return True
    return False


def validate_urls(urls: list[str], doc_id: str) -> None:
    """
    Validates a list of URLs for empty, duplicate, and malformed entries.

    param: list[str] urls : A list of urls
    param: str doc_id: The document id of the invalid source url/s
    raises ValueError: If the list contains duplicate, empty or malformed url/s
    """
    if contains_empty_urls(urls):
        raise ValueError(
            f"Empty URL found in list of translated urls. DocumentId : {doc_id}"
        )
    if contains_duplicate_urls(urls):
        raise ValueError(
            f"Duplicate URLs found in list of translated urls. DocumentId : {doc_id}"
        )
    if contains_invalid_paths(urls):
        raise ValueError(
            f"Malformed url found in list of translated urls. DocumentId : {doc_id}"
        )


def map_translated_files(translated_files_row: pd.Series) -> list[dict]:
    """
    Maps the GCF document with translated versions into the new json structure

    :param pd.Series translated_files_row: A row from the DataFrame containing the 'Translated files' field, which holds a string of translated source URLs separated by the pipe (|) character. This string includes multiple URLs for translated documents in various languages.
    :return: A list of mcf document objects, each with a different source url reflecting the translated version of the original document
    """

    mapped_documents = []

    concatenated_string_of_url_docs = str(
        translated_files_row[DocumentColumns.TRANSLATED_FILES.value]
    )
    url_docs = concatenated_string_of_url_docs.split("|")

    doc_id = translated_files_row.iloc[0]

    try:
        validate_urls(url_docs, doc_id)
        for url in url_docs:
            mapped_documents.append(
                {
                    "metadata": {
                        "type": translated_files_row[DocumentColumns.TYPE.value]
                    },
                    "title": translated_files_row[DocumentColumns.TITLE.value],
                    "source_url": url.strip(),
                    "variant_name": "Translated",
                }
            )
        return mapped_documents
    except Exception as e:
        raise e


def document(mcf_docs: pd.DataFrame, debug: bool) -> list[Optional[dict[str, Any]]]:
    """Map the GCF document info to new structure.

    :param pd.DataFrame mcf_docs: The MCF documents data.
    :param bool debug: Whether debug mode is on.
    :raises ValueError: If the DataFrame is missing one or more of the required column headers
    :return list[Optional[dict[str, Any]]]: A list of GCF families in
        the 'destination' format described in the GCF Data Mapper Google
        Sheet.
    """

    required_columns = [column.value for column in DocumentColumns]
    missing_columns = [col for col in required_columns if col not in mcf_docs.columns]

    if missing_columns:
        click.echo("Missing required columns: {}".format(", ".join(missing_columns)))
        raise ValueError("Missing required columns in MCF data frame")

    if debug:
        click.echo("📝 Wrangling GCF document data.")

    mapped_docs = []
    # We iterate over each row in the DataFrame mcf_docs using iterrows(),
    # the underscore indicates that the index of the row will not be used in this loop.
    # We check if the field in the 'TRANSLATED_TITLES' column is not NaN. Note - Empty entries return as nan
    # Then we create a dictionary for each row with metadata type, title, source URL,
    # and variant name.
    # If the field contains a value we will map a separate object for each of the translated
    # files using the translated url as the source url
    for _, row in mcf_docs.iterrows():
        has_translated_files = pd.notna(row.at[DocumentColumns.TRANSLATED_TITLES.value])
        mapped_docs.append(
            {
                "metadata": {"type": row[DocumentColumns.TYPE.value]},
                "title": row[DocumentColumns.TITLE.value],
                "source_url": row[DocumentColumns.SOURCE_URL.value],
                "variant_name": "Original Translation",
            }
        )
        if has_translated_files:
            mapped_docs.extend(map_translated_files(row))
    return mapped_docs
