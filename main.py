from pathlib import Path
import subprocess
from typing import Optional

import typer

from packages import Package
from network import download_binary, fetch_registry
from storage import get_bin_dir, init_dir_structure, load_config, load_packages, save_packages

app = typer.Typer()

def dimmify(text: str) -> str:
    return typer.style(text, dim=True)

@app.callback()
def startup():
    init_dir_structure()

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


if __name__ == "__main__":
    app()