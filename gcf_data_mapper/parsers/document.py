from typing import Any, Optional, cast
from urllib.parse import urlparse

import click
import pandas as pd

from gcf_data_mapper.enums.document import (
    DocumentVariantNames,
    IgnoreDocumentTypes,
    OptionalDocumentColumns,
    RequiredDocumentColumns,
    RequiredFamilyDocumentColumns,
)
from gcf_data_mapper.parsers.helpers import (
    check_required_column_value_not_na,
    verify_required_fields_present,
)


def contains_duplicate_urls(urls: list[str]) -> bool:
    """
    Check a list of urls for any duplicate entries.

    param: list[str] urls: A list of urls
    return bool: Returns true if duplicate urls are present, False
        otherwise.
    """

    # Convert all URLs to lowercase for case-insensitive comparison
    lowercase_urls = [url.lower() for url in urls]
    return len(lowercase_urls) != len(set(lowercase_urls))


def contains_empty_urls(urls: list[str]) -> bool:
    """
    Check a list of urls for any empty entries.

    param: list[str] urls: a list of urls
    return bool: Returns true if empty urls are present, or false if not
    """
    for url in urls:
        if not url.strip():
            return True
    return False


def contains_invalid_paths(urls: list[str]) -> bool:
    """
    Check a list of urls for any malformed entries.

    param: list[str] urls: A list of urls
    return bool: Returns true if malformed urls are present, or false
        if not
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


def validate_urls(urls: list[str], doc_id: str) -> Optional[bool]:
    """
    Validate a list of URLs for empty, duplicate, & malformed entries.

    param: list[str] urls : A list of urls
    param: str doc_id: The document id of the invalid source urls
    raises ValueError: If the list contains duplicate, empty or,
        malformed urls
    return Optional[bool]: None if one or more of the URls for the given
        document ID are invalid, otherwise True.
    """
    if contains_empty_urls(urls):
        click.echo(
            f"🛑 Empty URL found in list of translated urls. DocumentId : {doc_id}"
        )
        return

    if contains_duplicate_urls(urls):
        click.echo(
            f"🛑 Duplicate URLs found in list of translated urls. DocumentId : {doc_id}"
        )
        return

    if contains_invalid_paths(urls):
        click.echo(
            f"🛑 Malformed url found in list of translated urls. DocumentId : {doc_id}"
        )
        return
    return True


def has_translated_files(row: pd.Series) -> bool:
    """
    Check if the row has translated files.

    :param pd.Series row: The row to check.
    :return bool: True if translated files exist, False otherwise.
    """
    return pd.notna(row.at[OptionalDocumentColumns.TRANSLATED_TITLES.value])


def map_document_metadata(
    row: pd.Series,
    variant_name: str,
    source_url: Optional[str] = None,
) -> dict[str, Any]:
    """
    Create a document dictionary with common fields.

    :param pd.Series row: A record to map to a GCF document.
    :param str variant_name: The variant name.
    :param Optional[str] source_url: The source URL, defaults to None.
    :return dict[str, Any]: A dictionary representing the GCF doc.
    """
    approved_ref = row.at[RequiredFamilyDocumentColumns.APPROVED_REF.value]
    projects_id = row.at[RequiredFamilyDocumentColumns.PROJECTS_ID.value]

    doc_id = row[RequiredDocumentColumns.ID.value]
    doc_type = row[RequiredDocumentColumns.TYPE.value]
    title = row[RequiredDocumentColumns.TITLE.value]

    if source_url is None:
        source_url = cast(str, row[OptionalDocumentColumns.SOURCE_URL.value])

    return {
        "import_id": f"GCF.document.{approved_ref}_{projects_id}.{doc_id}",
        "family_import_id": f"GCF.family.{approved_ref}.{projects_id}",
        "metadata": {"type": doc_type},
        "title": title,
        "source_url": source_url.strip(),
        "variant_name": variant_name,
    }


def map_translated_files(
    translated_files_row: pd.Series,
) -> Optional[list[dict[str, Any]]]:
    """
    Map the GCF document with translated versions into JSON.

    :param pd.Series translated_files_row: A row from the DataFrame
        containing the 'Translated files' field.
    :return Optional[list[dict]]: A list of gcf document objects, each
        with a different source url reflecting the translated version of
        the original document. Returns None if one or more of the URLs
        in the Translated files is invalid.
    """

    mapped_documents = []
    url_docs = str(
        translated_files_row[OptionalDocumentColumns.TRANSLATED_FILES.value]
    ).split("|")
    doc_id = translated_files_row.at[RequiredDocumentColumns.ID.value]

    if validate_urls(url_docs, doc_id) is None:
        return None

    for url in url_docs:
        mapped_documents.append(
            map_document_metadata(
                translated_files_row,
                DocumentVariantNames.TRANSLATION.value,
                url,
            )
        )
    return mapped_documents


def process_row(row: pd.Series, debug: bool) -> Optional[list[dict[str, Any]]]:
    """Process a single row of document data.

    :param pd.Series row: The row of data to process (corresponds to a
        GCF document entry).
    :param bool debug: Whether debug mode is on.
    :return list[Optional[dict[str, Any]]]: A list of GCF documents in
        the 'destination' format described in the GCF Data Mapper Google
        Sheet.
    """
    doc_id = row.at[RequiredDocumentColumns.ID.value]
    if not check_required_column_value_not_na(row, RequiredFamilyDocumentColumns):
        click.echo(f"🛑 Skipping row with missing required family columns: {doc_id}")
        return None

    if not check_required_column_value_not_na(row, RequiredDocumentColumns):
        click.echo(f"🛑 Skipping row with missing required document columns: {doc_id}")
        return None

    mapped_docs = [map_document_metadata(row, DocumentVariantNames.ORIGINAL.value)]
    if has_translated_files(row):
        translated_docs = map_translated_files(row)
        if translated_docs is not None:
            mapped_docs.extend(translated_docs)

    return mapped_docs


def document(
    projects_data: pd.DataFrame, gcf_docs: pd.DataFrame, debug: bool
) -> list[Optional[dict[str, Any]]]:
    """Map the GCF document info to new structure.

    :param pd.DataFrame projects_data: The MCF and GCF project data,
        joined on FP num.
    :param pd.DataFrame gcf_docs: The GCF document data in a df.
    :param bool debug: Whether debug mode is on.
    :return list[Optional[dict[str, Any]]]: A list of GCF documents in
        the 'destination' format described in the GCF Data Mapper Google
        Sheet, or an empty list.
    """

    if debug:
        click.echo("📝 Wrangling GCF document data.")

    verify_required_fields_present(
        gcf_docs, {str(e.value) for e in RequiredDocumentColumns}
    )
    verify_required_fields_present(
        gcf_docs, {str(e.value) for e in OptionalDocumentColumns}
    )
    verify_required_fields_present(
        projects_data, {str(e.value) for e in RequiredFamilyDocumentColumns}
    )

    combo = pd.merge(
        left=gcf_docs,
        right=projects_data,
        left_on="FP number",
        right_on=RequiredFamilyDocumentColumns.APPROVED_REF.value,
        how="left",
    ).convert_dtypes()

    if debug:
        click.echo(f"📊 {combo.shape[0]} GCF documents in file...")

    combo = combo[
        ~combo[RequiredDocumentColumns.TYPE.value].isin(
            {e.value for e in IgnoreDocumentTypes}
        )
    ]

    if debug:
        click.echo(f"📊 Mapping {combo.shape[0]} GCF documents in phase 1...")

    mapped_docs = []
    for _, row in combo.iterrows():
        result = process_row(row, debug)
        if result:
            mapped_docs.extend(result)

    return mapped_docs
