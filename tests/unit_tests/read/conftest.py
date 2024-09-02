import os

import pytest

UNIT_TESTS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES_FOLDER = os.path.join(UNIT_TESTS_FOLDER, "fixtures")


@pytest.fixture(scope="module")
def fixtures_folder():
    return FIXTURES_FOLDER
