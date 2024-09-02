from enum import Enum
from typing import Any, Optional

import click
import pandas as pd


class DocumentColumns(Enum):
    TRANSLATED_FILES = "Translated files"
    TYPE = "Type"
    TITLE = "Title"
    SOURCE_URL = "Document page permalink"


def map_translated_files(translated_files_row: pd.Series) -> list[dict]:
    """
    Maps the GCF document with translated versions into the new json structure

    :param pd.Series translated_files_row: A row from the DataFrame containing the 'Translated files' field, which holds a string of translated source URLs separated by the pipe (|) character. This string includes multiple URLs for translated documents in various languages.
    :return: A list of mcf document objects, each with a different source url reflecting the translated version of the original document
    """

    mapped_documents = []

    files_string = str(translated_files_row["Translated files"])
    list_of_translated_doc_urls = files_string.split("|")

    for url in list_of_translated_doc_urls:
        mapped_documents.append(
            {
                "metadata": {"type": translated_files_row[DocumentColumns.TYPE.value]},
                "title": translated_files_row[DocumentColumns.TITLE.value],
                "source_url": url,
                "variant_name": "Translated",
            }
        )
    return mapped_documents


def document(mcf_docs: pd.DataFrame, debug: bool) -> list[Optional[dict[str, Any]]]:
    """Map the GCF document info to new structure.

    :param pd.DataFrame mcf_docs: The MCF documents data.
    :param bool debug: Whether debug mode is on.
    :return list[Optional[dict[str, Any]]]: A list of GCF families in
        the 'destination' format described in the GCF Data Mapper Google
        Sheet.
    """
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
