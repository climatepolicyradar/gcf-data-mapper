import csv

import click


@click.group()
def cli():
    pass


def read_csv(file_path: str):
    with open(file_path, "r") as file:
        csv_reader = csv.DictReader(file)
        data = []
        for line in csv_reader:
            data.append(line["country"])
        click.echo(data)


def read_json(file_path: str):
    with open(file_path, "r") as file:
        data = file.read()
        click.echo(data)


@click.command("read_data_file")
@click.argument("file_path", type=click.Path(exists=True))
def read_data_file(file_path: str):
    """Read the data file"""
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


def entrypoint():
    cli.add_command(read_data_file)
    cli()


if __name__ == "__main__":
    entrypoint()
