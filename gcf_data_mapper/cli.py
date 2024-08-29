import os
import sys
from typing import Any, Optional

import click
import pandas as pd

from gcf_data_mapper.parsers.collection import collection
from gcf_data_mapper.parsers.document import document
from gcf_data_mapper.parsers.family import family
from gcf_data_mapper.read import read


@click.command()
@click.option(
    "--gcf_projects_file",
    default=os.path.join(os.getcwd(), "data", "gcf-projects.json"),
    type=click.Path(exists=True),
)
@click.option(
    "--mcf_projects_file",
    # trunk-ignore(cspell/error)
    default=os.path.join(os.getcwd(), "data", "MCFprojects.csv"),
    type=click.Path(exists=True),
)
@click.option(
    "--mcf_docs_file",
    # trunk-ignore(cspell/error)
    default=os.path.join(os.getcwd(), "data", "MCFdocuments-v2.csv"),
    type=click.Path(exists=True),
)
@click.option(
    "--output_file",
    default=os.path.join(os.getcwd(), "output.json"),
    type=click.Path(exists=False),
)
@click.option("--debug/--no-debug", default=True)
@click.version_option("0.1.0", "--version", "-v", help="Show the version and exit.")
def entrypoint(
    gcf_projects_file, mcf_projects_file, mcf_docs_file, output_file, debug: bool
):
    """Simple program that wrangles GCF data into bulk import format.

    :param str gcf_projects_file: The GCF projects filename.
    :param str mcf_projects_file: The MCF projects filename.
    :param str mcf_docs_file: The MCF projects filename.
    :param str output_file: The output filename.
    :param bool debug: Whether debug mode is on.
    """
    click.echo("🚀 Starting the GCF data mapping process.")
    if debug:
        click.echo("📝 Input files:")
        click.echo(f"- {click.format_filename(gcf_projects_file)}")
        click.echo(f"- {click.format_filename(mcf_projects_file)}")
        click.echo(f"- {click.format_filename(mcf_docs_file)}")

    try:
        project_info, doc_info = read(
            gcf_projects_file, mcf_projects_file, mcf_docs_file, debug
        )
        mapped_data = wrangle_to_json(project_info, doc_info, debug)
    except Exception as e:
        click.echo(f"❌ Failed to map GCF data to expected JSON. Error: {e}.")
        sys.exit(1)

    click.echo("✅ Finished mapping GCF data.")

    click.echo()
    click.echo("🚀 Dumping GCF data to output file")
    dump_output(mapped_data, output_file, debug)
    click.echo("✅ Finished dumping mapped GCF data.")


def wrangle_to_json(
    project_info: pd.DataFrame, doc_info: pd.DataFrame, debug: bool
) -> dict[str, list[Optional[dict[str, Any]]]]:
    """Put the mapped GCF data into a dictionary ready for dumping.

    The output of this function will get dumped as JSON to the output
    file.

    :param pd.DataFrame project_info: The GCF and MCF joined project
        info.
    :param pd.DataFrame doc_info: The MCF docs info.
    :param bool debug: Whether debug mode is on.
    :return dict[str, list[Optional[dict[str, Any]]]]: The GCF data
        mapped to the Document-Family-Collection-Event entity it
        corresponds to.
    """
    return {
        "collections": collection(debug),
        "families": family(project_info, debug),
        "documents": document(doc_info, debug),
        "events": [],
    }


def dump_output(
    mapped_data: dict[str, list[Optional[dict[str, Any]]]],
    output_file: str,
    debug: bool,
):
    """Dump the wrangled JSON to the output file.

    :param dict[str, list[Optional[dict[str, Any]]]] mapped_data: The
        mapped GCF data.
    :param str output_file: The output filename.
    :param bool debug: Whether debug mode is on.
    """
    if debug:
        click.echo(f"📝 Output file {click.format_filename(output_file)}")


if __name__ == "__main__":
    entrypoint()
