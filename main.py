# stdlib imports
import os
from pathlib import Path
import subprocess
import sys
import platform
import tempfile
from typing import Optional

# third-party imports
import requests
import typer
from rich.progress import Progress
from rich.console import Console

# local imports
from packages import Package
from network import download_binary, fetch_registry, get_file_size
from storage import get_bin_dir, get_config_path, init_dir_structure, load_config, load_packages, save_packages

__version__ = "0.2.0-alpha.1"

def version_callback(value: bool):
    if value:
        typer.echo(typer.style(f"Centi Package Manager (centipm) version {__version__}", fg=typer.colors.BRIGHT_CYAN, bold=True))
        raise typer.Exit()

app = typer.Typer(
    context_settings={
        "help_option_names": ['-h', '--help']
    },
    add_completion=False,
    no_args_is_help=True
)

def log_load(message: str, task, dim: bool = False):
    """Runs a task with a LOAD spinner"""
    console = Console()
    
    with console.status(
        typer.style(f"LOAD ", fg=typer.colors.BRIGHT_BLUE, bold=not dim) + 
        typer.style(message, dim=dim)
    ):
        result = task()
    return result

def log(message: str, level: str = "INFO", bold: bool = False, dim: bool = False) -> None:
    color_map = {
        "INFO": typer.colors.CYAN,
        "LOAD": typer.colors.BRIGHT_BLUE,
        "FAIL": typer.colors.BRIGHT_RED,
        "DONE": typer.colors.BRIGHT_GREEN,
        "WARN": typer.colors.BRIGHT_YELLOW,
        "GUIDE": typer.colors.YELLOW,
        "NOTE": typer.colors.BRIGHT_CYAN
    }
    color = color_map.get(level, typer.colors.WHITE)
    styled_message = typer.style(level, fg=color, bold=bold, dim=dim)
    message = typer.style(message, bold=bold, dim=dim)
    typer.echo(f"{styled_message} {message}")

def dimmify(text: str) -> str:
    return typer.style(text, dim=True)

@app.callback()
def startup(
    version: bool = typer.Option(
        None,
        "--version", "-v", 
        callback=version_callback, 
        is_eager=True,
        help="Shows the CentiPM version and exit"
    ),
):
    init_dir_structure()

@app.command()
def registry():
    """Shows the registry URL"""
    config = load_config()
    registry_url = config["registry"]["url"]
    typer.echo(typer.style(f"Current registry URL: ", fg=typer.colors.BRIGHT_CYAN, bold=True), nl=False)
    typer.echo(registry_url)

@app.command()
def config():
    """Shows the config file path"""
    typer.echo(typer.style(f"Config file path: ", fg=typer.colors.BRIGHT_CYAN, bold=True), nl=False)
    typer.echo(get_config_path())

@app.command()
def install(package: str, version: str = "latest", dim: bool = typer.Option(False, "--dim/--no-dim", help="Dim the output instead of showing it in bright colors")):
    """Installs a package"""
    log(f"Finding '{package}' version {version}...", level="LOAD", bold=not dim, dim=dim)
    registry_url = load_config()["registry"]["url"]
    registries = fetch_registry(registry_url)

    if package in load_packages():
        log("Package already installed!", level="FAIL", bold=True) # TODO: Implement reinstall command
        return
    if package not in registries:
        log("Package doesn't exist in the registry!", level="FAIL", bold=not dim, dim=dim)
        log("If this package exists in another registry, please modify the registry URL inside ~/.centipm/config.toml", level="GUIDE", dim=dim)
        return

    # TODO: Versions

    log(f"Found '{package}'! Installing...", level="LOAD", bold=not dim, dim=dim)
    
    file_size = get_file_size(registries[package].url)
    if file_size > 0:
        with Progress(transient=True) as progress:
            task = progress.add_task("Downloading...", total=file_size)
            download_binary(
                package,
                registries[package].url,
                on_progress=lambda size: progress.update(task, advance=size)
            )
    else:
        console = Console()
        with console.status("Downloading..."):
            download_binary(package, registries[package].url)

    log(f"Successfully installed '{package}'!", level="INFO", bold=not dim, dim=dim)
    log("Saving entry..", level="LOAD", bold=not dim, dim=dim)

    new_packages = load_packages()
    new_packages[registries[package].name] = registries[package].to_package()
    save_packages(new_packages)
    log(f"Successfully installed '{package}'! Run it with 'centipm run {package}'", level="DONE", bold=not dim, dim=dim)

@app.command()
def remove(package: str, dim: bool = typer.Option(False, "--dim/--no-dim", help="Dim the output instead of showing it in bright colors")):
    """Removes an installed package"""
    log(f"Finding {package}...", level="LOAD", bold=not dim, dim=dim)
    if package not in load_packages():
        log(f"Package '{package}' is not installed!", level="FAIL", bold=not dim, dim=dim)
        return
    
    log(f"Found '{package}'!", level="INFO", bold=not dim, dim=dim)
    log(f"Removing {package}...", level="LOAD", bold=not dim, dim=dim)
    (get_bin_dir() / package).unlink()
    log(f"Removing entry...", level="LOAD", bold=not dim, dim=dim)

    log(f"Saving entry..", level="LOAD", bold=not dim, dim=dim)
    new_packages = load_packages()
    del new_packages[package]
    save_packages(new_packages)
    log(f"Successfully removed '{package}'!", level="DONE", bold=not dim, dim=dim)

@app.command()
def view():
    """Lists the installed packages"""
    packages = load_packages()
    if not packages:
        log("No installed packages yet, get some using the 'install' command!", level="WARN", bold=True)
        return

    for package, info in packages.items():
        typer.echo(typer.style(f"{info.author}/", fg=typer.colors.BRIGHT_BLUE, bold=True), nl=False)
        typer.echo(typer.style(f"{package} ", bold=True), nl=False)
        typer.echo(typer.style(info.version, fg=typer.colors.BRIGHT_GREEN, bold=True))
        typer.echo(f"    {info.description}")

@app.command()
def search(query: str, author: bool = typer.Option(False, "--author", help="Search by author instead of package name and description")):
    """Searches for a package in the registry"""
    log(f"Searching for '{query}' in the registry...", level="LOAD", bold=True)
    registry_url = load_config()["registry"]["url"]
    registries = fetch_registry(registry_url)

    results = []
    for name, info in registries.items():
        if not author:
            if query.lower() in name.lower() or query.lower() in info.description.lower():
                results.append((name, info))
        else:
            if query.lower() in info.author.lower():
                results.append((name, info))
    
    if not results:
        log(f"No results found for '{query}'!", level="WARN", bold=True)
        return
    
    log(f"Found {len(results)} result(s) for '{query}':", level="INFO", bold=True)
    for name, info in results:
        typer.echo(typer.style(f"{info.author}/", fg=typer.colors.BRIGHT_BLUE, bold=True), nl=False)
        typer.echo(typer.style(f"{name} ", bold=True), nl=False)
        typer.echo(typer.style(info.version, fg=typer.colors.BRIGHT_GREEN, bold=True))
        typer.echo(f"    {info.description}")

@app.command(
    context_settings={
        "allow_extra_args": True, 
        "ignore_unknown_options": True,
        "help_option_names": ['-h']
    }
)
def run(package: str, extra: Optional[list[str]] = typer.Argument(None)):
    """Execute an installed package"""
    if package not in load_packages():
        log(f"Package '{package}' is not installed!", level="FAIL", bold=True)
        return
    if not Path.exists(get_bin_dir() / package):
        log(f"Binary for '{package}' is missing!", level="FAIL", bold=True)
        log("This shouldn't happen, unless the files was manually removed.", level="GUIDE")
        log("If this was unintentional, please submit an issue on the GitHub repository of this project!", level="GUIDE")
        log("This is not the fault of the package, do not submit an issue to the package binary unless completely sure.", level="GUIDE")
        return
    subprocess.run([str(get_bin_dir() / package)] + (extra or []))

@app.command()
def reinstall(package: str, version: str = "latest", dim: bool = typer.Option(False, "--dim/--no-dim", help="Dim the output instead of showing it in bright colors")):
    """Reinstalls a package"""
    remove(package, dim=dim)
    install(package, version, dim=dim)

@app.command()
def update(package: Optional[str] = None):
    """Updates a package or all packages if no package is specified"""
    registries = fetch_registry(load_config()["registry"]["url"])
    packages = load_packages()

    if not packages:
        log("No installed packages yet, get some using the 'install' command!", level="WARN", bold=True)
        return

    if package:
        if package not in packages:
            log(f"Package '{package}' is not installed!", level="FAIL", bold=True)
            return
        if package not in registries:
            log(f"Package '{package}' doesn't exist in the registry!", level="FAIL", bold=True)
            return
        
        if registries[package].version == load_packages()[package].version:
            log(f"Package '{package}' is up-to-date!", level="WARN", bold=True)
            if typer.confirm("Reinstall anyway?"):
                reinstall(package, dim=True)
                log(f"Successfully reinstalled '{package}'!", level="DONE", bold=True)
            return
        
        reinstall(package, dim=True)
        log(f"Successfully updated '{package}'!", level="DONE", bold=True)
    
    if not package:
        log("Executing full upgrade", level="NOTE", bold=True)
        typer.echo("This will try to update all installed packages.")
        if not typer.confirm("Continue?", default=True):
            log("Process aborted.", level="FAIL", bold=True)
            return
        
        # Iiiit's design question time! Should we prompt the user for literally every package that's up-to-date?
        # : Probably not. We should prompt the user for all reinstallation or ignore up-to-date packages
        # Huh, great instinct, UX designer me!
        # : Thanks. You should probably get to coding.
        # Oh shoot!
        # : The default should be Y!
        # Who knew I had a good UX brain.

        dont_reinstall = typer.confirm("Skip reinstallation of up-to-date packages?", default=True)
        
        # Hey thinking me, how do we show "No updates installed" if all packages are up-to-date?
        # : We can use a flag to check if any package was updated, and if not, show the message at the end.
        # Great idea, let's do that!

        any_updated: bool = False
        for package in packages:
            if registries[package].version == packages[package].version:
                if not dont_reinstall: 
                    log(f"Package '{package}' is up-to-date! Reinstalling anyway..", level="WARN", bold=True)
                    reinstall(package, dim=True)
                    log(f"Reinstalled '{package}'!", level="DONE", bold=True)
                    any_updated = True
                continue
            
            # If it DOESN'T match (previous check uses continue)
            reinstall(package, dim=True)
            log(f"Successfully updated '{package}'!", level="DONE", bold=True)
            any_updated = True

        if not any_updated:
            log("No updates installed.", level="NOTE", bold=True)

@app.command(name="update-self")
def update_self(prerelease: bool = typer.Option(False, "--pre-release", help="Include prerelease versions in the update check")):
    """Updates CentiPM itself to the latest version on GitHub releases"""

    platform_map = {
        "Linux": "centipm-linux",
        "Darwin": "centipm-macos",
        "Windows": "centipm-windows"
    }
    system = platform.system()
    if system not in platform_map:
        log(f"Unsupported platform: {system}", level="FAIL", bold=True)
        log("Wha- how did you get this error? I thought I covered all platforms!", level="GUIDE")
        log("Please submit an issue on the GitHub repository of this project, including the output of 'platform.system()' and 'platform.version()'!", level="GUIDE")
        log("Seriously though, CentiPM should work on any platform with Python 3.14. Maybe install the Linux (manually, I'm sorry) version in the meantime?", level="GUIDE")
        return

    target_name = platform_map[system]
    asset_url = None

    if not typer.confirm("This will update CentiPM itself. Continue?", default=True):
        log("Process aborted.", level="FAIL", bold=True)
        return
    
    target_release_type = "pre-release" if prerelease else "release"

    if prerelease:
        typer.echo("Pre-release versions may be unstable. This flag will check for the absolutely newest release, including pre-releases.")
        if not typer.confirm("Continue? ", default=True): # set to true because the user already used the flag
            log("Skipping pre-release scans..", level="INFO", bold=True)
            target_release_type = "release"

    match target_release_type:
        case "pre-release":
            response = requests.get("https://api.github.com/repos/tyydev1/centipm/releases")
            response.raise_for_status()
            releases = response.json()

            if not releases:
                log("No releases found!", level="FAIL", bold=True)
                return
            
            json = releases[0]

        case "release":
            response = requests.get("https://api.github.com/repos/tyydev1/centipm/releases/latest")
            response.raise_for_status()

            json = response.json()

    latest_version = json["tag_name"]
    if latest_version.lstrip("v") == __version__:
        log(f"You are already using the latest version of CentiPM ({__version__})!", level="NOTE", bold=True)
        return
    
    for asset in json["assets"]:
        if asset["name"] == target_name:
            asset_url = asset["browser_download_url"]
            break

    if not asset_url:
        log(f"Could not find asset for platform '{system}'!", level="FAIL", bold=True)
        log("For the meantime, you can manually download the binary for the closest-like platform in the GitHub releases page, like Linux.", level="GUIDE")
        return

    temp_path = Path(tempfile.gettempdir()) / "centipm_update"
    log(f"Updating CentiPM from version {__version__} to {latest_version}...", level="LOAD", bold=True)
    download_binary(
        "centipm",   
        asset_url,
        dest=temp_path
    ) # updated this function to take an optional dest param, defaulted to the bin directory
    os.replace(temp_path, sys.executable)

    log("Successfully updated CentiPM! Please restart your terminal (though you don't need to) to apply the update.", level="DONE", bold=True)

if __name__ == "__main__":
    app()