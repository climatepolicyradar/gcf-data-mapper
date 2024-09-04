from typing import Any, Optional, cast
from urllib.parse import urlparse

import click
import pandas as pd

from gcf_data_mapper.enums.document import (
    IgnoreDocumentTypes,
    RequiredDocumentColumns,
    RequiredFamilyDocumentColumns,
)


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
    :return: A list of gcf document objects, each with a different source url reflecting the translated version of the original document
    """

    mapped_documents = []

    concatenated_string_of_url_docs = str(
        translated_files_row[RequiredDocumentColumns.TRANSLATED_FILES.value]
    )
    url_docs = concatenated_string_of_url_docs.split("|")

    doc_id = translated_files_row.at[RequiredDocumentColumns.ID.value]

    approved_ref = translated_files_row.at[
        RequiredFamilyDocumentColumns.APPROVED_REF.value
    ]

    projects_id = translated_files_row.at[
        RequiredFamilyDocumentColumns.PROJECTS_ID.value
    ]

    try:
        validate_urls(url_docs, doc_id)
        for url in url_docs:
            mapped_documents.append(
                {
                    "import_id": f"GCF.document.{approved_ref}_{projects_id}.{doc_id}",
                    "family_import_id": f"GCF.family.{approved_ref}.{projects_id}",
                    "metadata": {
                        "type": translated_files_row[RequiredDocumentColumns.TYPE.value]
                    },
                    "title": translated_files_row[RequiredDocumentColumns.TITLE.value],
                    "source_url": url.strip(),
                    "variant_name": "Translated",
                }
            )
        return mapped_documents
    except Exception as e:
        raise e


def document(
    projects_data: pd.DataFrame, gcf_docs: pd.DataFrame, debug: bool
) -> list[Optional[dict[str, Any]]]:
    """Map the GCF document info to new structure.

    :param pd.DataFrame projects_data: The MCF and GCF project data,
        joined on FP num.
    :param pd.DataFrame gcf_docs: The GCF documents data.
    :param bool debug: Whether debug mode is on.
    :raises ValueError: If the DataFrame is missing one or more of the
        required column headers
    :return list[Optional[dict[str, Any]]]: A list of GCF families in
        the 'destination' format described in the GCF Data Mapper Google
        Sheet.
    """
    required_columns = [column.value for column in RequiredDocumentColumns]
    missing_columns = [col for col in required_columns if col not in gcf_docs.columns]

    if missing_columns:
        raise ValueError(
            f"Missing required columns {missing_columns} in GCF data frame"
        )

    if debug:
        click.echo("📝 Wrangling GCF document data.")
        click.echo(f"📝 {gcf_docs.shape[0]} GCF documents to map...")

    # Left join the document data with the GCF projects data so we can determine the
    # project a document should be associated with. We then need to filter out certain
    # GCF document types for now until Phase 2, TODO.After this, convert the values
    # in the Projects ID column to be integers so we don't end up with 5 parts to our
    # import IDs (as there is full stop in float values when they're converted to str).
    combo = pd.merge(
        left=gcf_docs,
        right=projects_data,
        left_on="FP number",
        right_on=RequiredFamilyDocumentColumns.APPROVED_REF.value,
        how="left",
    )
    combo = combo[
        ~combo[RequiredDocumentColumns.TYPE.value].isin(
            [e.value for e in IgnoreDocumentTypes]
        )
    ]
    combo[RequiredFamilyDocumentColumns.PROJECTS_ID.value] = cast(
        pd.DataFrame, combo[RequiredFamilyDocumentColumns.PROJECTS_ID.value]
    ).convert_dtypes()

    if debug:
        click.echo(combo)

    mapped_docs = []

    # We iterate over each row in the DataFrame gcf_docs using iterrows(),
    # the underscore indicates that the index of the row will not be used in this loop.
    # We check if the field in the 'TRANSLATED_TITLES' column is not NaN. Note - Empty entries return as nan
    # Then we create a dictionary for each row with metadata type, title, source URL,
    # and variant name which is appended to the list.
    # Separately, if that row also contains a value in the translated titles column,
    # we will map a separate object for each of the translated versions, using the translated url
    # as the source url and add those translated versions to the list
    for _, row in combo.iterrows():
        document_id = row.at[RequiredDocumentColumns.ID.value]

        approved_ref = row.at[RequiredFamilyDocumentColumns.APPROVED_REF.value]
        projects_id = row.at[RequiredFamilyDocumentColumns.PROJECTS_ID.value]

        if not all([pd.notna(approved_ref), pd.notna(projects_id)]):
            click.echo(f"🛑 No project data associated with document ID {document_id}")
            continue

        has_translated_files = pd.notna(
            row.at[RequiredDocumentColumns.TRANSLATED_TITLES.value]
        )
        mapped_docs.append(
            {
                "import_id": f"GCF.document.{approved_ref}_{projects_id}.{document_id}",
                "family_import_id": f"GCF.family.{approved_ref}.{projects_id}",
                "metadata": {"type": row[RequiredDocumentColumns.TYPE.value]},
                "title": row[RequiredDocumentColumns.TITLE.value],
                "source_url": row[RequiredDocumentColumns.SOURCE_URL.value],
                "variant_name": "Original Translation",
            }
        )
        if has_translated_files:
            mapped_docs.extend(map_translated_files(row))
    return mapped_docs
