import csv
import sys

import click


@click.group()
@click.version_option("0.1.0", "--version", "-v", help="Show the version and exit.")
def cli():
    pass


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


@click.command("read_data_file")
@click.argument("file_path", type=click.Path(exists=True))
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


@click.command()
def wrangle_json():
    """Simple program that wrangles GCF data into bulk import format."""
    click.echo("🚀 Starting the GCF data mapping process.")

    try:
        collection()
    except Exception as e:
        click.echo(f"❌ Failed to map GCF data to expected JSON. Error: {e}.")
        sys.exit(1)

    click.echo("✅ Finished mapping GCF data.")


def collection():
    """Map the GCF collection info to new structure.

    Collection information is not currently available for GCF data, so
    we will leave this function as not implemented for now.
    """
    pass


def entrypoint():
    cli.add_command(read_data_file)
    cli.add_command(wrangle_json)
    cli()


if __name__ == "__main__":
    entrypoint()
