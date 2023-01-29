import sys
from pathlib import Path

import pytest  # noqa


def pytest_configure():
    package_path = Path(__file__).resolve().parents[1]
    sys.path.append(str(package_path))
