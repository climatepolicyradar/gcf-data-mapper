# Instructions for the developer

## Install pyenv

```bash

# Install pyenv
curl https://pyenv.run | bash

# Add pyenv to your shell
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Install a specific version of Python
pyenv install 3.11.5  # Example version

# Set the local version of Python for the project
pyenv local 3.11.5
```

## Install poetry

```bash

# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add poetry to your path if not already added
export PATH="$HOME/.local/bin:$PATH"

# Navigate to the project directory and install dependencies
cd say_hello
poetry install
```
