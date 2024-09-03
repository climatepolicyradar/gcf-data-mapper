.DEFAULT_GOAL := help

.PHONY: help
help: ## Display this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install_trunk: ## Install trunk
	$(eval trunk_installed=$(shell trunk --version > /dev/null 2>&1 ; echo $$? ))
ifneq (${trunk_installed},0)
	$(eval OS_NAME=$(shell uname -s | tr A-Z a-z))
	curl https://get.trunk.io -fsSL | bash
endif

uninstall_trunk: ## Uninstall trunk
	sudo rm -if `which trunk`
	rm -ifr ${HOME}/.cache/trunk

share_trunk:
	trunk init

move_workflows: ## Move workflows to .github/workflows
	mv workflows .github/workflows

init: share_trunk move_workflows

setup_with_pyenv: ## Setup the project with pyenv
	pyenv install 3.10
	pyenv virtualenv 3.10 gcf-dm
	pyenv activate gcf-dm
	poetry install

install_git_hooks: install_trunk
	trunk init

check: ## Format and check the project with trunk
	trunk fmt
	trunk check

build: ## Build the project
	poetry build

test: ## Run tests using pytest
	poetry run pytest -v

test_coverage: ## Run tests using pytest with coverage
	poetry run coverage run -m pytest -vvv tests
	coverage report

test_coverage_html: test_coverage ## Run tests using pytest with coverage and generate a HTML report
	coverage report
