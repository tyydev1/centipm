<div align="center">

# CentiPM

**A compact, standalone environmental package manager.**

</div>

---

# Disclaimer(s)

- CentiPM is currently in very early development. Expect many bugs, missing features, and breaking changes. Use at your own risk.
- CentiPM (currently) is only test supported on Linux, and may not work properly on other platforms. I will try to add support for other platforms in the future, but for now, Linux is the only officially supported platform. If you want to use CentiPM on an unsupported platform, you can try it out and see if it works, but keep in mind that it may not work properly, and you may encounter bugs and issues that I am not aware of.

- CentiPM is a binary package manager, which means that it installs packages as pre-compiled binaries. It does not compile packages from source code, nor does it have any support for package dependencies (yet) and archive formats (e.g. .zip, .tar.gz, etc.). It simply downloads the binary file from the registry and saves it to the bin directory.
- I am working on adding support for package dependencies and archive formats, but it is not a priority at the moment. The current focus is on getting the core functionality of installing and upgrading packages working smoothly, and then adding additional features later on. Keep in mind that I am the sole developer of this project, and I am working on it in my free time, so progress may be slow and unpredictable. If you want to contribute to the project, please feel free to submit a pull request or open an issue with your ideas and suggestions.

- CentiPM is not affiliated with any other package manager or registry. It is a completely independent project, and does not use any existing package manager or registry as a backend. It is built from the ground up, with the goal of being as simple and lightweight as possible.
- CentiPM is not intended to replace existing package managers, but rather to provide a simple and lightweight alternative for users who want to manage their packages without the overhead of a full-fledged package manager. It is designed to be used alongside existing package managers, and can coexist with them without any issues.


# Installation

## Supported Platforms
**CENTIPM IS ONLY TEST SUPPORTED ON LINUX!**

- **Linux** (tested on CachyOS, aka my distro that I coded this on, but should work on any modern Linux distro)
- *MacOS* (untested, but should work as long as Python 3.14 is installed, and because it's very similar to Linux (.sh scripts should work fine))

## Unsupported Platforms (but should work in theory)

- **Windows**: untested, very experimental and may not work at all, but should work in theory as long as Python 3.14 is installed, and because it's just downloading binaries, it should be able to download .exe files and run them without any issues)

## 1. Releases

Go to the [Releases](https://github.com/tyydev1/centipm/releases) page (if it exists yet), and download the attached binary or the source code.

### Attached Binary
Run this command:

```bash
chmod +x <path-to-centipm-binary>
```

You can run it directly (requires explicit path), or assign it to your PATH. (Look it up, I'm not explaining how to put stuff in PATH)

### Source Code
Unzip the source code, and run `pip install .` in the root directory. This will install the `centipm` command globally, and you can run it from anywhere.

## 2. Build from source

Clone this github repository,

```bash
git clone https://github.com/tyydev1/centipm.git
cd centipm
```

Then run `pip install .` in the root directory. This will install the `centipm` command globally, and you can run it from anywhere.

# Usage

Run `centipm --help` to see the available commands and options. The most basic usage is `centipm install <package>`, which will install a package from the registry. You can also run `centipm upgrade` to upgrade all installed packages, or `centipm upgrade --package <package>` to upgrade a specific package.

**List of available and planned commands (checkmarked means complete):**
- [x] `install <package>`: Installs a package from the registry.
- [x] `update [--package <package>]`: Upgrades all installed packages or a specific package if `--package` is provided.
- [x] `view`: Lists all installed packages.
- [x] `registry`: Shows the registry URL, 
- [x] `config`: Shows the config file path.
- [x] `remove <package>`: Uninstalls a package.
- [ ] `search <query>`: Searches for packages in the registry matching the query.
- [x] `run <package> [args...]`: Runs the binary of the specified package with optional arguments.
- [ ] `registry add <registry_url>`: Adds a new registry URL to the config file.
- [ ] `registry remove <registry_url>`: Removes a registry URL from the config file

# Adding your own registries

By default, CentiPM uses a registry hosted at `https://raw.githubusercontent.com/tyydev1/centipm/main/registries.toml`. However, you can add your own registries by modifying the `config.toml` file located in the CentiPM configuration directory (default at `~/.centipm/config.toml`).

Your registry URL should point to a `registries.toml` file that follows the same format as the default registry. Once you've added your registry URL to the config file, CentiPM will fetch packages from it during installation and upgrades, just like that.

## Registry Fields

Read the comments in the [default registries.toml](https://github.com/tyydev1/centipm-registry/blob/main/registries.toml) file for a guide on the required fields and format for adding packages to your registry.

# To-do List
- [x] Implement basic package manager functionality (installing, upgrading, listing, removing packages).
- [ ] Implement unchecked features in the usage section (e.g. search, registry management).
- [ ] Add support for package dependencies.
- [ ] Add support for archive formats (e.g. .zip, .tar.gz, etc.).
- [ ] Add support for multiple registries and registry prioritization.
- [ ] Add support for package versioning and version constraints.

# Contributing

Contributions are welcome! If you want to contribute, please fork the repository and create a pull request with your changes. Make sure to follow the existing code style and include tests for any new functionality.