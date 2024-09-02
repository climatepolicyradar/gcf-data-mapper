from typing import Any, Optional

import click


def collection(debug: bool) -> list[Optional[dict[str, Any]]]:
    """Map the GCF collection info to new structure.

    Collection information is not currently available for GCF data, so
    we will leave this function as not implemented for now.

    :param bool debug: Whether debug mode is on.
    :return list[Optional[dict[str, Any]]]: A list of GCF families in
        the 'destination' format described in the GCF Data Mapper Google
        Sheet.
    """
    if debug:
        click.echo("📝 No GCF collection data to wrangle.")

    return []
