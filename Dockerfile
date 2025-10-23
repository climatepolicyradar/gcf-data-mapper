# checkov:skip=CKV_DOCKER_2
FROM python:3.10-slim

# Create a non-root user
RUN useradd -m -u 1000 gcf_data_mapper_user

# This ensures that the dependencies are installed at system python level
# without having to activate a venv
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# Install uv (fast Python dependency manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Copy your source code
COPY gcf_data_mapper gcf_data_mapper

# Install dependencies using the lockfile
RUN uv sync --frozen

# Switch to non-root user
USER gcf_data_mapper_user

# We are skipping the healthcheck because it is not needed for the Prefect agent
# since this is a CLI tool and not a service that needs to be monitored
# we also don't have a health endpoint to ping to provide a meaningful healthcheck
