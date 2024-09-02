# gcf-data-mapper

A CLI tool to map the GCF data to the required JSON format for bulk-import.

- _Developers_ please read the [DEVELOPERS.md](DEVELOPERS.md) file for more
  information.

- This tool is designed to map this [GCF data](https://drive.google.com/drive/folders/1FBia9JzpdaCjRe7M7-pgh3Ahl9_MReh_)

## Installation

This package is not available on PyPI. To install it, you need to build the
package and install it locally.

```bash
make build # Ensure you have the package built

# Install the package into your environment
poetry run pip install dist/gcf_data_mapper-<version>-py3-none-any.whl
```

Goto the [releases page](https://github.com/climatepolicyradar/gcf-data-mapper/releases)
to find the latest version.

## Usage

If `--output_file` is not passed, by default an output file called `output.json`
will be created in the current directory if it does not already exist.

If `--gcf_projects_file`, `mcf_projects_file` or `mcf_docs_file` is not passed,
by default the GCF mapper tool will look for a sub-folder in the current working
directory called `data` with the following files in it:

```bash
gcf_data_mapper --gcf_projects_file FILENAME --mcf_projects_file FILENAME --mcf_docs_file FILENAME --output_file FILENAME
```
