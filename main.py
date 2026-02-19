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

# local imports
from packages import Package
from network import download_binary, fetch_registry
from storage import get_bin_dir, get_config_path, init_dir_structure, load_config, load_packages, save_packages

__version__ = "0.1.0"

def version_callback(value: bool):
    if value:
        typer.echo(typer.style(f"Centi Package Manager (centipm) version {__version__}", fg=typer.colors.BRIGHT_CYAN, bold=True))
        raise typer.Exit()

app = typer.Typer(
    context_settings={
        "help_option_names": ['-h', '--help']
    }
)

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
    if not dim:
        typer.echo(typer.style(f"[LOAD] Finding '{package}' version {version}...", fg=typer.colors.BRIGHT_BLUE, bold=True))
    else:
        typer.echo(dimmify(f"[LOAD] Finding '{package}' version {version}..."))
    registry_url = load_config()["registry"]["url"]
    registries = fetch_registry(registry_url)

    if package in load_packages():
        typer.echo(typer.style("[FAIL] Package already installed!", fg=typer.colors.BRIGHT_RED, bold=True)) # TODO: Implement reinstall command
        return
    if package not in registries:
        if not dim:
            typer.echo(typer.style("[FAIL] Package doesn't exist in the registry!", 
                                   fg=typer.colors.BRIGHT_RED, 
                                   bold=True))
            typer.echo(typer.style("[GUIDE] If this package exists in another registry, please modify"
                                   " the registry URL inside ~/.centipm/config.toml",
                                   fg=typer.colors.YELLOW))
        else:
            typer.echo(dimmify("[FAIL] Package doesn't exist in the registry!"))
            typer.echo(dimmify("[GUIDE] If this package exists in another registry, please modify"
                               " the registry URL inside ~/.centipm/config.toml"))
        return

    # TODO: Versions
    if not dim:
        typer.echo(typer.style(f"[LOAD] Found '{package}'! Installing...", fg=typer.colors.BRIGHT_BLUE, bold=True))
    else:
        typer.echo(dimmify(f"[LOAD] Found '{package}'! Installing..."))
    download_binary(package, registries[package].url)
    if not dim:
        typer.echo(typer.style(f"[LOAD] Successfully installed '{package}'! Saving entry..", fg=typer.colors.BRIGHT_BLUE, bold=True))
    else:
        typer.echo(dimmify(f"[LOAD] Successfully installed '{package}'! Saving entry.."))

    new_packages = load_packages()
    new_packages[registries[package].name] = registries[package].to_package()
    save_packages(new_packages)
    if not dim:
        typer.echo(typer.style(f"[DONE] Successfully installed '{package}'! Run it with 'centipm run {package}'", fg=typer.colors.BRIGHT_GREEN, bold=True))
    else:
        typer.echo(dimmify(f"[DONE] Successfully installed '{package}'! Run it with 'centipm run {package}'"))

@app.command()
def remove(package: str, dim: bool = typer.Option(False, "--dim/--no-dim", help="Dim the output instead of showing it in bright colors")):
    """Removes an installed package"""
    if not dim:
        typer.echo(typer.style(f"[LOAD] Finding {package}...", fg=typer.colors.BRIGHT_BLUE, bold=True))
    else:
        typer.echo(dimmify(f"[LOAD] Finding {package}..."))
    if package not in load_packages():
        if dim:
            typer.echo(dimmify(f"[FAIL] Package '{package}' is not installed!"))
        else:
            typer.echo(typer.style(f"[FAIL] Package '{package}' is not installed!", fg=typer.colors.BRIGHT_RED, bold=True))
        return
    
    if not dim:
        typer.echo(typer.style(f"[LOAD] Found '{package}'! Removing...", fg=typer.colors.BRIGHT_BLUE, bold=True))
    else:
        typer.echo(dimmify(f"[LOAD] Found '{package}'! Removing..."))
    (get_bin_dir() / package).unlink()
    if not dim:
        typer.echo(typer.style(f"[LOAD] Successfully removed '{package}'! Removing entry...", fg=typer.colors.BRIGHT_BLUE, bold=True))
    else:
        typer.echo(dimmify(f"[LOAD] Successfully removed '{package}'! Removing entry..."))

    new_packages = load_packages()
    del new_packages[package]
    save_packages(new_packages)
    if not dim:
        typer.echo(typer.style(f"[DONE] Successfully removed '{package}'!", fg=typer.colors.BRIGHT_GREEN, bold=True))
    else:
        typer.echo(dimmify(f"[DONE] Successfully removed '{package}'!"))

@app.command()
def view():
    """Lists the installed packages"""
    packages = load_packages()
    if not packages:
        typer.echo(typer.style(
            "No installed packages yet, get some using the 'install' command!",
            fg=typer.colors.BRIGHT_YELLOW,
            bold=True
        ))
        return

    for package, info in packages.items():
        typer.echo(
            typer.style(
                f"{package} ",
                bold=True
            ), 
            nl=False
        )
        typer.echo(
            typer.style(
                info.version,
                fg=typer.colors.BRIGHT_GREEN,
                bold=True
            )
        )
        
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
        typer.echo(typer.style(f"[FAIL] Package '{package}' is not installed!", fg=typer.colors.BRIGHT_RED, bold=True))
        return
    if not Path.exists(get_bin_dir() / package):
        typer.echo(typer.style(f"[FAIL] Binary for '{package}' is missing!", fg=typer.colors.BRIGHT_RED, bold=True))
        typer.echo(typer.style("[GUIDE] This shouldn't happen, unless the files was manually removed.\n"
                               "[GUIDE] If this was unintentional, please submit an issue on the GitHub repository of this project!\n"
                               "[GUIDE] This is not the fault of the package, do not submit an issue to the package binary unless completely sure.",
                               fg=typer.colors.YELLOW))
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

    if package:
        if package not in packages:
            typer.echo(typer.style(f"[FAIL] Package '{package}' is not installed!", fg=typer.colors.BRIGHT_RED, bold=True))
            return
        if package not in registries:
            typer.echo(typer.style(f"[FAIL] Package '{package}' doesn't exist in the registry!", fg=typer.colors.BRIGHT_RED, bold=True))
            return
        
        if registries[package].version == load_packages()[package].version:
            typer.echo(typer.style(f"[WARN] Package '{package}' is up-to-date!", fg=typer.colors.BRIGHT_YELLOW, bold=True))
            if typer.confirm("Reinstall anyway?"): # I dug and found this feature myself!
                reinstall(package, dim=True)
                typer.echo(typer.style(f"[DONE] Successfully reinstalled '{package}'!", fg=typer.colors.BRIGHT_GREEN, bold=True))
            return
        
        reinstall(package, dim=True)
        typer.echo(typer.style(f"[DONE] Successfully updated '{package}'!", fg=typer.colors.BRIGHT_GREEN, bold=True))
    
    if not packages:
        typer.echo(typer.style(
            "No installed packages yet, get some using the 'install' command!",
            fg=typer.colors.BRIGHT_YELLOW,
            bold=True
        ))
        return
    
    if not package:
        typer.echo(typer.style("[NOTE] Executing full upgrade", fg=typer.colors.CYAN, bold=True))
        typer.echo("This will try to update all installed packages.")
        if not typer.confirm("Continue?", default=True):
            typer.echo(typer.style("[FAIL] Process aborted.", fg=typer.colors.BRIGHT_RED, bold=True))
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
                    typer.echo(typer.style(f"[WARN] Package '{package}' is up-to-date! Reinstalling anyway..", fg=typer.colors.BRIGHT_YELLOW, bold=True))
                    reinstall(package, dim=True)
                    typer.echo(typer.style(f"[DONE] Reinstalled '{package}'!", fg=typer.colors.BRIGHT_GREEN, bold=True))
                    any_updated = True
                continue
            
            # If it DOESN'T match (previous check uses continue)
            reinstall(package, dim=True)
            typer.echo(typer.style(f"[DONE] Successfully updated '{package}'!", fg=typer.colors.BRIGHT_GREEN, bold=True))
            any_updated = True

        if not any_updated:
            typer.echo(typer.style("[NOTE] No updates installed.", fg=typer.colors.BRIGHT_CYAN, bold=True))

@app.command(name="update-self")
def update_self():
    """Updates CentiPM itself to the latest version on GitHub releases"""

    platform_map = {
        "Linux": "centipm-linux",
        "Darwin": "centipm-macos",
        "Windows": "centipm-windows"
    }
    system = platform.system()
    if system not in platform_map:
        typer.echo(typer.style(f"[FAIL] Unsupported platform: {system}", fg=typer.colors.BRIGHT_RED, bold=True))
        typer.echo(typer.style("[GUIDE] Wha- how did get this error? I thought I covered all platforms!", fg=typer.colors.YELLOW))
        typer.echo(typer.style("[GUIDE] Please submit an issue on the GitHub repository of this project, including the output of 'platform.system()' and 'platform.version()'!", fg=typer.colors.YELLOW))
        typer.echo(typer.style("[GUIDE] Seriously though, CentiPM should work on any platform with Python 3.14. Maybe install the Linux (manually, I'm sorry) version in the meantime?", fg=typer.colors.YELLOW))
        return

    target_name = platform_map[system]
    asset_url = None

    if not typer.confirm("This will update CentiPM itself. Continue?", default=True):
        typer.echo(typer.style("[FAIL] Process aborted.", fg=typer.colors.BRIGHT_RED, bold=True))
        return
    
    response = requests.get("https://api.github.com/repos/tyydev1/centipm/releases/latest")
    response.raise_for_status()

    json = response.json()
    latest_version = json["tag_name"]
    if latest_version.lstrip("v") == __version__:
        typer.echo(typer.style(f"[NOTE] You are already using the latest version of CentiPM ({__version__})!", fg=typer.colors.BRIGHT_CYAN, bold=True))
        return
    
    for asset in json["assets"]:
        if asset["name"] == target_name:
            asset_url = asset["browser_download_url"]
            break

    if not asset_url:
        typer.echo(typer.style(f"[FAIL] Could not find asset for platform '{system}'!", fg=typer.colors.BRIGHT_RED, bold=True))
        typer.echo(typer.style("[GUIDE] For the meantime, you can manually download the binary for the closest-like platform in the GitHub releases page, like Linux.", fg=typer.colors.YELLOW))
        return

    temp_path = Path(tempfile.gettempdir()) / "centipm_update"
    typer.echo(typer.style(f"[LOAD] Updating CentiPM from version {__version__} to {latest_version}...", fg=typer.colors.BRIGHT_BLUE, bold=True))
    download_binary(
        "centipm",   
        asset_url,
        dest=temp_path
    ) # updated this function to take an optional dest param, defaulted to the bin directory
    os.replace(temp_path, sys.executable)

    typer.echo(typer.style("[DONE] Successfully updated CentiPM! Please restart your terminal (though you don't need to) to apply the update.", fg=typer.colors.BRIGHT_GREEN, bold=True))

if __name__ == "__main__":
    app()