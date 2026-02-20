<div align="center">

# CentiPM

**A compact, standalone ~~package~~ binary manager.**

</div>

---

# Disclaimer(s)

- CentiPM is currently in very early development. Expect many bugs, missing features, and breaking changes. Use at your own risk.
- CentiPM (currently) is only tested on Linux, and may not work properly on other platforms.
- If you encounter instructions that say they use Python 3.14, that's because it's my working Python version, but if it works with something below, please let me know, so I can update the documentation and lower the required Python version.

- CentiPM is a binary package manager, which means that it installs packages as pre-compiled binaries. It does not compile packages from source code, nor does it have any support for package dependencies (yet) and archive formats (e.g. .zip, .tar.gz, etc.). It simply downloads the binary file from the registry and saves it to the bin directory.
- I am working on adding support for stuff on the [To-do List](#to-do-list), do keep in mind that I am a solo developer and I am doing this in my free time.

- CentiPM is not affiliated with any other package manager or registry.
- CentiPM is not intended to replace existing package managers (but you totally can).

# Why You Should Use CentiPM

Honestly, you shouldn't, at least not yet. CentiPM is in very early development, and it is more of a learning project for me to practice and have fun coding. If this project turns out the way I hope it will, then it may be a good alternative. Stay tuned.

# Installation

## Supported Platforms
**CENTIPM IS ONLY TESTED ON LINUX!**

- **Linux** (tested on CachyOS, aka my distro that I coded this on, but should work on any modern Linux distro)
- ~~macOS~~ (untested, but should work as long as Python ~3.14 is installed, and because it's very similar to Linux (.sh scripts should work fine))

## Unsupported Platforms (experimental)

- **Windows**: untested, very experimental and may not work at all, but should work in theory with Python ~3.14, and because it's just downloading binaries, it should be able to download .exe files, but Paths are a bit messy. Though some binaries on the registry may not have Windows support, do not submit an issue to this repository, submit it to the registry repository instead.

## 1. Releases

Go to the [Releases](https://github.com/tyydev1/centipm/releases) page (if it exists yet), and download the attached binary or the source code.

### Attached Binary
Run this command:

```bash
chmod +x <path-to-centipm-binary>
```

From there, you can rename the binary to `centipm` for easier use, and move it to a directory in your PATH (e.g. `/usr/local/bin` on Linux). If you're a little weewee here's the command for that:

```bash
mv <path-to-centipm-binary> /usr/local/bin/centipm
```

### Source Code
Unzip the source code, and run `pip install .` in the root directory. This will install the `centipm` command globally, and you can run it from anywhere.

**BEWARE**: Look the warning below in the [Build from Source](#2-build-from-source) section, as the `update-self` command may not work properly if you install using this method.

## 2. Build from source

Clone this github repository,

```bash
git clone https://github.com/tyydev1/centipm.git
cd centipm
```

Then run `pip install .` in the root directory. This will install the `centipm` command globally, and you can run it from anywhere.

**BEWARE**: The `update-self` command may not work properly if you install using this method. I highly recommend using the attached binary from the releases page if you want to use the `update-self` command, as it is designed to update the binary itself, and the releases still show pre-release versions, so you can still get the latest features and updates without having to build from source.

# Usage

Run `centipm --help` to see the available commands and options. The most basic usage is `centipm install <package>`, which will install a package from the registry. You can also run `centipm update` to upgrade all installed packages, or `centipm update --package <package>` to upgrade a specific package.

To put all your binaries to PATH (though I don't recommend this, you can just use the `centipm run <package>` command), you can add the following line to your shell configuration file (e.g. `~/.bashrc` or `~/.zshrc`):

```bash
export PATH="$HOME/.centipm/bin:$PATH"
```

**List of available and planned commands (checkmarked means complete):**
- [x] `install <package>`: Installs a package from the registry.
- [x] `update [--package <package>]`: Upgrades all installed packages or a specific package if `--package` is provided.
- [x] `view`: Lists all installed packages.
- [x] `registry`: Shows the registry URL, 
- [x] `config`: Shows the config file path.
- [x] `remove <package>`: Uninstalls a package.
- [x] `search <query>`: Searches for packages in the registry matching the query.
- [x] `run <package> [args...]`: Runs the binary of the specified package with optional arguments.
- [ ] `registry add <registry_url>`: Adds a new registry URL to the config file.
- [ ] `registry remove <registry_url>`: Removes a registry URL from the config file
- [ ] `registry list`: Lists all registry URLs in the config file.
- [x] `update-self`: Updates CentiPM itself to the latest version.
- [x] `changelog`: Shows the changelog of the latest version.

# Adding your own registries

By default, CentiPM uses a registry hosted at `https://raw.githubusercontent.com/tyydev1/centipm/main/registries.toml`. However, you can add your own registries by modifying the `config.toml` file located in the CentiPM configuration directory (default at `~/.centipm/config.toml`).

NOTICE: Soon, the default registry will be moved to a separate github repository, and the `registries.toml` file will be removed from this repository.

Your registry URL should point to a `registries.toml` file that follows the same format as the default registry. Once you've added your registry URL to the config file, CentiPM will fetch packages from it during installation and upgrades, just like that.

## Registry Fields

Read the comments in the [default registries.toml](https://github.com/tyydev1/dime-centipm-registry/blob/main/registries.toml) file for a guide on the required fields and format for adding packages to your registry.

# Security Warning

The latest stable version of CentiPM currently does not implement integrity verification (e.g., SHA256 checks). Use trusted registries only. It is up to the user to ensure that they trust the registries they are using. Don't worry, I am working on adding sha256 hash verification for downloaded packages to ensure integrity and security, but for now, just be careful.

It is recommended to just use the default registry (Dime/CentiPM Registry), as it is maintained by me and I will try my best to ensure that it only contains safe and trustworthy packages. If you want to use a custom registry, make sure to review the packages in it before installing them.

### Security Relief

*The latest alpha version or above, 0.3.0-alpha.1, has successfully implemented SHA256 integrity verification.*

# To-do List 
### (Pre-rc releases that already implement these will not affect the to-do list.)
- [x] Implement basic package manager functionality (installing, upgrading, listing, removing packages).
- [ ] Implement unchecked features in the usage section (e.g. registry management).
- [ ] Add `runner` field on the registry fields for script files.
- [ ] Downgrade Python version as low as possible without sacrificing any functionality, so your ~~smart fridge~~ device can run it too.
- [ ] Add sha256 hash verification for downloaded packages to ensure integrity and security.
- [ ] Add a Rust extention module early (via PyO3) for improved performance.
- [ ] Add support for archive formats (e.g. .zip, .tar.gz, etc.).
- [ ] Add support for multiple registries and registry prioritization.
- [ ] Add support for package dependencies.
- [ ] Add support for package versioning and version constraints.

# Contributing

Contributions are welcome! If you want to contribute, please fork the repository and create a pull request with your changes. Make sure to follow the existing code style and include tests for any new functionality.

# License

This project is protected under the MIT License. See the [LICENSE](LICENSE) file for more details.

Cheers,
tyydev1

---

## Future Projects (very planned)
- [ ] millicent-dime - centipm shrunk down. A micro package manager that only supports installing and removing packages, and has a smaller binary size. But, it supports Dime's registry format, so it can use the same registry as CentiPM, and it can be a good alternative for users who want a smaller and simpler package manager.
- [ ] rscentipm - a completely Rust implementation of CentiPM, which will be faster and more efficient than the Python version. This is the last thing on the to-do list because it suggests that this project is already complete and fully-featured, which is not the case yet.