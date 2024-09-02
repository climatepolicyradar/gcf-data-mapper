from enum import Enum
from typing import Any, Optional
from urllib.parse import urlparse

import click
import pandas as pd


class DocumentColumns(Enum):
    TRANSLATED_FILES = "Translated files"
    TYPE = "Type"
    TITLE = "Title"
    SOURCE_URL = "Document page permalink"


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


def contains_malformed_urls(urls: list[str]) -> bool:
    """
    Checks a list of urls for any malformed entries

    param: list[str] urls: A list of urls
    return bool: Returns true if malformed urls are present, or false if not
    """
    malformed_urls_exist = False
    for url in urls:
        if url.strip() and not urlparse(url).scheme:
            malformed_urls_exist = True
    return malformed_urls_exist


def validate_urls(urls: list[str], doc_id: str) -> None:
    """
    Validates a list of URLs for empty, duplicate, and malformed entries.

    param: urls list[str] : A list of urls
    param: doc_id str: The document id of the invalid source url/s
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
    if contains_malformed_urls(urls):
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

    files_string = str(translated_files_row["Translated files"])
    list_of_translated_doc_urls = files_string.split("|")

    # trunk-ignore(cspell/error)
    doc_id = translated_files_row.iloc[0]

    try:
        validate_urls(list_of_translated_doc_urls, doc_id)
        for url in list_of_translated_doc_urls:
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
        raise ValueError from e


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
    # trunk-ignore(cspell/error)
    for _, row in mcf_docs.iterrows():
        # trunk-ignore(cspell/error)
        has_translated_files = pd.notna(row.at["Translated files"])
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
