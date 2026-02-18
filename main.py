import typer

app = typer.Typer()

@app.command()
def install(package: str, version: str = "latest"):
    """Installs a package"""
    print(f"Installing {package} version {version}...")

@app.command()
def remove(package: str):
    """Removes an installed package"""
    print(f"Removing {package}...")

@app.command()
def view():
    """Lists the installed packages"""
    print("Showing installed packages..")

@app.command()
def run(package: str):
    """Execute an installed package"""
    print(f"Running {package}...")

if __name__ == "__main__":
    app()