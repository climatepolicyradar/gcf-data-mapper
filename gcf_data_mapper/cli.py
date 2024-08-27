import csv
import sys
from typing import Any, Optional

import click

from gcf_data_mapper.parsers.collection import collection


@click.command()
@click.argument("file_path", type=click.Path(exists=True))
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
        "documents": [],
        "events": [],
    }

def read_csv(file_path: str):
    """Reads a csv file, we will just read the file for now and echo a value"""
    with open(file_path, "r") as file:
        csv_reader = csv.DictReader(file)
        data = []
        for line in csv_reader:
            data.append(line["country"])
        click.echo(data)


def read_json(file_path: str):
    """Reads a json file, we will just read the file for now and echo a value"""
    with open(file_path, "r") as file:
        data = file.read()
        click.echo(data)

def read_data_file(file_path: str):
    """Simple program that reads a data file, calls a function to read a csv or json file respectively"""
    file_extension = file_path.lower().split(".")[-1]
    try:
        if file_extension not in ["json", "csv"]:
            raise ValueError("File must be a valid json or csv file")
        if file_extension == "csv":
            read_csv(file_path)
        elif file_extension == "json":
            read_json(file_path)
    except Exception as e:
        click.echo(f"Error reading file: {e}")


def dump_output():
    pass


if __name__ == "__main__":
    entrypoint()