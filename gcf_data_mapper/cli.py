import sys
from typing import Any, Optional

import click

from gcf_data_mapper.parsers.collection import collection
from gcf_data_mapper.parsers.document import document
from gcf_data_mapper.parsers.family import family


@click.command()
@click.option("--debug/--no-debug", default=False)
@click.version_option("0.1.0", "--version", "-v", help="Show the version and exit.")
def entrypoint(debug: bool):
    """Simple program that wrangles GCF data into bulk import format.

    :param bool debug: Whether debug mode is on.
    """
    click.echo("🚀 Starting the GCF data mapping process.")

    try:
        wrangle_to_json(debug)
    except Exception as e:
        click.echo(f"❌ Failed to map GCF data to expected JSON. Error: {e}.")
        sys.exit(1)

    click.echo("✅ Finished mapping GCF data.")

    click.echo()
    click.echo("🚀 Dumping GCF data to output file")
    dump_output()
    click.echo("✅ Finished dumping mapped GCF data.")


def wrangle_to_json(debug) -> dict[str, list[Optional[dict[str, Any]]]]:
    """Put the mapped GCF data into a dictionary ready for dumping.

    The output of this function will get dumped as JSON to the output
    file.

    :param bool debug: Whether debug mode is on.
    :return dict[str, list[Optional[dict[str, Any]]]]: The GCF data
        mapped to the Document-Family-Collection-Event entity it
        corresponds to.
    """
    return {
        "collections": collection(debug),
        "families": family(debug),
        "documents": document(debug),
        "events": [],
    }


def dump_output():
    pass


if __name__ == "__main__":
    entrypoint()
