from functools import lru_cache

import toml

from app.common.utils.path import get_root_path


@lru_cache
def get_project_version() -> str:
    """
    Get the project version from the pyproject.toml file

    :return: The project version
    """
    root_path = get_root_path()
    parsed_result = toml.load(root_path / "pyproject.toml")
    return str(parsed_result["project"]["version"])
