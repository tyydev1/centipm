# This file contains the functions responsible for network-related issues, such as
# fetching files from the registry URL, connecting to the URL, and more.

from pathlib import Path
import tomllib
import os
import stat
from typing import Optional

from storage import get_bin_dir
from packages import RegistryPackage
import requests

def fetch_registry(url: str) -> dict[str, RegistryPackage]:
    response = requests.get(url)
    response.raise_for_status()
    
    registry = tomllib.loads(response.text)
    return {
        name: RegistryPackage.from_dict(name, data) for name, data in registry.items()
    }

def get_file_size(url: str) -> int:
    response = requests.head(url)
    return int(response.headers.get("Content-Length", 0))

def download_binary(name: str, 
                    url: str, 
                    dest: Optional[Path | str] = None,
                    on_progress=None) -> None:
    if dest is None:
        dest = str(get_bin_dir() / name)

    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192): # 8KB
            f.write(chunk)
            if on_progress:
                on_progress(len(chunk))

    os.chmod(dest, os.stat(dest).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # TODO: QoL feature; silently test run the file, if a certain error code
    # is returned (what's the code for that), we alarm the user with a WARN log.

