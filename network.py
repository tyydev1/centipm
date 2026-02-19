# This file contains the functions responsible for network-related issues, such as
# fetching files from the registry URL, connecting to the URL, and more.

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

def download_binary(name: str, url: str, dest: Optional[str] = None) -> None:
    if dest is None:
        dest = str(get_bin_dir() / name)

    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest, "wb") as f: # is this right? do we use name here?
        for chunk in response.iter_content(chunk_size=8192): # 8KB
            f.write(chunk)

    os.chmod(dest, os.stat(dest).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # TODO: QoL feature; silently test run the file, if a certain error code
    # is returned (what's the code for that), we alarm the user with a WARN log.


