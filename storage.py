# This file contains the functions responsible for storage-related purposes, such as fetching file location,
# unzipping ZIP files, moving files into specific directories, and even creating those directories.

from pathlib import Path

def init() -> None:
    root = Path.home() / ".centipm"
    root.mkdir(parents=True, exist_ok=True)

    bin_dir = root / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    packages_reg = root / "packages.json"
    packages_reg.touch(exist_ok=True)

def get_root() -> Path:
    return Path.home() / ".centipm"

def get_bin_dir() -> Path:
    return get_root() / "bin"

def get_packreg_path() -> Path:
    return get_root() / "packages.json"

# For now, this is the functions of this file. I will end this session, and add
# the following features in the future, TODO:
# 1. Loading and saving the packages.json file

