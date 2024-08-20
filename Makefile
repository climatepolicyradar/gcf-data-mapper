install_trunk:
	$(eval trunk_installed=$(shell trunk --version > /dev/null 2>&1 ; echo $$? ))
ifneq (${trunk_installed},0)
	$(eval OS_NAME=$(shell uname -s | tr A-Z a-z))
	curl https://get.trunk.io -fsSL | bash
endif

uninstall_trunk:
	sudo rm -if `which trunk`
	rm -ifr ${HOME}/.cache/trunk

share_trunk:
	trunk init

move_workflows:
	mv workflows .github/workflows

init: share_trunk move_workflows

setup_with_pyenv:
	pyenv install 3.10
	pyenv virtualenv 3.10 gcf-dm
	pyenv activate gcf-dm
	poetry install

install_git_hooks: install_trunk
	trunk init
	trunk actions run configure-pyright

check:
	trunk fmt
	trunk check

build:
	poetry build

test:
	poetry run pytest
