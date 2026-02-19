# This file contains the functions responsible for storage-related purposes, such as fetching file location,
# unzipping ZIP files, moving files into specific directories, and even creating those directories.

import json
from pathlib import Path
import tomllib
from packages import Package

def init_dir_structure() -> None:
    root = Path.home() / ".centipm"
    root.mkdir(parents=True, exist_ok=True)

    bin_dir = root / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    if not (packreg_file := (root / "packages.json")).exists():
        with open(packreg_file, "w") as f:
            json.dump({}, f)

    if not (config_path := (root / "config.toml")).exists():
        with open(config_path, "w") as f:
            f.write("###--Automatically generated config file--###\n")
            f.write("# This file contains the configuration for centipm.\n")
            f.write("# You can edit this file to change the behavior of centipm.\n")
            f.write("# For example, you can change the registry URL here,\n")
            f.write("# to be your own registry, or a mirror of the official registry.\n")
            f.write("# You can read the registry syntax for making your own registry in the source code, or\n")
            f.write("# in the future documentation.\n")
            f.write("\n")
            f.write("[registry]\n")
            f.write('url = "https://raw.githubusercontent.com/tyydev1/centipm/main/registries.toml"\n')

def get_root() -> Path:
    return Path.home() / ".centipm"

def get_bin_dir() -> Path:
    return get_root() / "bin"

def get_packreg_path() -> Path:
    return get_root() / "packages.json"

def get_config_path() -> Path:
    return get_root() / "config.toml"

# This process could probably use the Rust language for loading
# a lot of packages.
def load_packages() -> dict[str, Package]:
    with open(get_packreg_path(), "r") as f:
        entries: dict[str, dict[str, str]] = json.load(f)
    return {
        name: Package.from_dict(name, entry) for name, entry in entries.items()
    }

def save_packages(packages: dict[str, Package]) -> None:
    with open(get_packreg_path(), "w") as f:
        json.dump({name: package.to_dict() for name, package in packages.items()}, f)

def load_config() -> dict[str, dict[str, str]]:
    with open(get_config_path(), "rb") as f:
        config = tomllib.load(f)
    return config
