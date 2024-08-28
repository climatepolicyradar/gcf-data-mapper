import os
import sys
from typing import Any, Optional

import click
import pandas as pd

from gcf_data_mapper.parsers.collection import collection
from gcf_data_mapper.parsers.document import document
from gcf_data_mapper.parsers.family import family
from gcf_data_mapper.read import read_data_file


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

    :param click.Path gcf_projects_file: The GCF projects filename.
    :param click.Path mcf_projects_file: The MCF projects filename.
    :param click.Path mcf_docs_file: The MCF projects filename.
    :param click.Path output_file: The output filename.
    :param bool debug: Whether debug mode is on.
    """

    click.echo("🚀 Starting the GCF data mapping process.")
    if debug:
        click.echo("📝 Input files:")
        click.echo(f"- {click.format_filename(gcf_projects_file)}")
        click.echo(f"- {click.format_filename(mcf_projects_file)}")
        click.echo(f"- {click.format_filename(mcf_docs_file)}")

    try:
        wrangle_to_json(gcf_projects_file, mcf_projects_file, mcf_docs_file, debug)
    except Exception as e:
        click.echo(f"❌ Failed to map GCF data to expected JSON. Error: {e}.")
        sys.exit(1)

    click.echo("✅ Finished mapping GCF data.")

    click.echo()
    click.echo("🚀 Dumping GCF data to output file")
    dump_output(output_file, debug)
    click.echo("✅ Finished dumping mapped GCF data.")


def wrangle_to_json(
    gcf_projects_file, mcf_projects_file, mcf_docs_file, debug: bool
) -> dict[str, list[Optional[dict[str, Any]]]]:
    """Put the mapped GCF data into a dictionary ready for dumping.

    The output of this function will get dumped as JSON to the output
    file.

    :param click.Path gcf_projects_file: The GCF projects filename.
    :param click.Path mcf_projects_file: The MCF projects filename.
    :param click.Path mcf_docs_file: The MCF projects filename.
    :param click.Path output_file: The output filename.
    :param bool debug: Whether debug mode is on.
    :return dict[str, list[Optional[dict[str, Any]]]]: The GCF data
        mapped to the Document-Family-Collection-Event entity it
        corresponds to.
    """
    gcf_projects: pd.DataFrame = read_data_file(gcf_projects_file)
    mcf_projects: pd.DataFrame = read_data_file(mcf_projects_file)
    mcf_docs: pd.DataFrame = read_data_file(mcf_docs_file)

    if any(
        data is None or data.empty for data in [gcf_projects, mcf_projects, mcf_docs]
    ):
        raise ValueError("One or more of the expected dataframes are empty")

    mcf_projects.rename(columns={"FP number": "ApprovedRef"}, inplace=True)
    project_info = pd.merge(
        left=gcf_projects,
        right=mcf_projects,
        # left_on="ApprovedRef",
        # right_on="FP number",
    )
    # merged_df.drop("team_name", axis=1, inplace=True)
    click.echo(project_info)

    return {
        "collections": collection(debug),
        "families": family(project_info, debug),
        "documents": document(mcf_docs, debug),
        "events": [],
    }


def dump_output(output_file, debug: bool):
    """Dump the wrangled JSON to the output file.

    :param click.Path output_file: The output filename.
    :param bool debug: Whether debug mode is on.
    """
    if debug:
        click.echo(f"📝 Output file {click.format_filename(output_file)}")


if __name__ == "__main__":
    entrypoint()
