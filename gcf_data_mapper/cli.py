import csv

import sys

import click


@click.command()
@click.version_option("0.1.0", "--version", "-v", help="Show the version and exit.")
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


if __name__ == "__main__":
    wrangle_json()
