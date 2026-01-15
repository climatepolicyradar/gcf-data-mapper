share_trunk:
	trunk init

install:
	uv sync --dev

replace_repo_name:
	sed -i 's/REPO_NAME_PLACEHOLDER/gcf-data-mapper/g' .github/workflows/ci-cd.yml

setup: install_git_hooks replace_repo_name install

install_git_hooks: install_git install_trunk share_trunk

initialise_git:
	git config --global init.defaultBranch main
	git init

build:
	docker build --tag gcf-data-mapper --platform="linux/amd64" .

test: ## Run tests using pytest
	poetry run pytest -vvv

test_coverage: ## Run tests using pytest with coverage
	poetry run coverage run -m pytest -vvv tests
	coverage report

test_coverage_html: test_coverage ## Run tests using pytest with coverage and generate a HTML report
	coverage report
