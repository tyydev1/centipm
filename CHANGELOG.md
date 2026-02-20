# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] 2026-02-20

### Added
- `author` field to the registry, which is shown in the search results and package info.
- `changelog` command to show the changelog of the latest version.
- (installed) tag in the search results to indicate which packages are already installed.
- Speaking of search results, `search` command is implemented now, which allows you to search for packages in the registry matching a query. The search results show the package name, version, description, and author.
- Added progress bars for downloading and fallback to a simple spinner if the content length is not provided by the server.
- Made cleaner logging (code internals) throughout the codebase, and added more logs for better debugging and user experience.

### Changed
- Registry now has a separate `author` field.

### Deprecated
- This repository's registry, the registries.toml file is moved to the [Dime/CentiPM Registry](https://github.com/tyydev1/dime-centipm-registry).

### Removed
- None for now.

### Fixed
- Fixed some bugs and edge cases in the codebase, and improved the overall stability and performance of the application.
- `update-self` command is now more robust and should work properly (previously it doesn't work at all)

### Security
- None for now.

## [0.1.0] - 2026-02-19

### Added
- Initial release

[0.2.0]: https://github.com/username/repo/compare/v0.2.0...HEAD
[0.1.0]: https://github.com/username/repo/releases/tag/v0.1.0
