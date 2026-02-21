# This file contains the functions responsible for network-related issues, such as
# fetching files from the registry URL, connecting to the URL, and more.

from pathlib import Path
import tomllib
import os
import stat
from typing import Optional
import hashlib

from storage import get_bin_dir
from packages import RegistryPackage
import requests


def verify_checksum(file_path: Path, expected_hash: str) -> bool:
    """Verifies the SHA256 checksum of the file at the given path against the expected hash."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest() == expected_hash

def fetch_registry(url: str) -> dict[str, RegistryPackage]:
    """Fetches the registry from the given URL and returns a dictionary of package names to RegistryPackage objects."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Could not connect to the registry. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        raise ConnectionError(f"Registry returned an error: {e.response.status_code}")
    except requests.exceptions.Timeout:
        raise ConnectionError("Registry request timed out.")
    
    registry = tomllib.loads(response.text)
    return {
        name: RegistryPackage.from_dict(name, data) for name, data in registry.items()
    }

def get_file_size(url: str) -> int:
    """Returns the size of the file at the given URL in bytes."""
    response = requests.head(url)
    return int(response.headers.get("Content-Length", 0))

def download_binary(name: str, 
                    url: str, 
                    dest: Optional[Path | str] = None,
                    on_progress=None) -> None:
    """Downloads a binary from the given URL and saves it to the specified destination. If no destination is provided, it saves it to the bin directory with the given name."""
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

