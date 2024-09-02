from typing import Any, Optional

import click
import pandas as pd


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

    return []
