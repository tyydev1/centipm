import typer

from packages import Package
from network import download_binary, fetch_registry
from storage import init_dir_structure, load_config, load_packages, save_packages

app = typer.Typer()

@app.callback()
def startup():
    init_dir_structure()

@app.command()
def install(package: str, version: str = "latest"):
    """Installs a package"""
    typer.echo(typer.style(f"[LOAD] Finding '{package}' version {version}...", fg=typer.colors.BRIGHT_BLUE, bold=True))
    registry_url = load_config()["registry"]["url"]
    registries = fetch_registry(registry_url)

    if package in load_packages():
        typer.echo(typer.style("[FAIL] Package already installed!", fg=typer.colors.BRIGHT_RED, bold=True)) # TODO: Implement reinstall command
        return
    if package not in registries:
        typer.echo(typer.style("[FAIL] Package doesn't exist in the registry!", 
                               fg=typer.colors.BRIGHT_RED, 
                               bold=True))
        typer.echo(typer.style("[GUIDE] If this package exists in another registry, please modify"
                               " the registry URL inside ~/.centipm/config.toml",
                               fg=typer.colors.YELLOW))
        return

    # TODO: Versions
    typer.echo(typer.style(f"[LOAD] Found '{package}'! Installing...", fg=typer.colors.BRIGHT_BLUE, bold=True))
    download_binary(package, registries[package].url)
    typer.echo(typer.style(f"[LOAD] Successfully installed '{package}'! Saving entry..", fg=typer.colors.BRIGHT_BLUE, bold=True))

    new_packages = load_packages()
    new_packages[registries[package].name] = registries[package].to_package()
    save_packages(new_packages)
    typer.echo(typer.style(f"[DONE] Successfully installed '{package}'! Run it with 'centipm run {package}'", fg=typer.colors.BRIGHT_BLUE, bold=True))

@app.command()
def remove(package: str):
    """Removes an installed package"""
    typer.echo(typer.style(f"[LOAD] Removing {package}...", fg=typer.colors.BRIGHT_RED, bold=True))

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
        
        typer.echo(f"\t{info.description}")

@app.command()
def run(package: str):
    """Execute an installed package"""
    typer.echo(f"Running {package}...")

if __name__ == "__main__":
    app()