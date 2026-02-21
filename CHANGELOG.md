# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0-beta.2] 2026-02-21

### *Everything on 0.3.0-beta.1, and..*

### Fixed
- A fatal bug on the packages class, causing `packages.json` to not have any entries.

## [0.3.0.beta.1] 2026-02-21

### *Everything on the 0.3.0-alpha versions, and...*

### Added
- `runner` field to the registries. This allows script files that are not standalone binaries to run correctly. The contents should be a string of the command, `"python"` for `.py`, `"node"` for `.js, ..`, and more. If the user doesn't have the feature, uhh I don't know. Will be resolved in 0.3.0 stable.

## [0.3.0-alpha.2] 2026-02-21

### Fixed
- `update-self` now works if centipm is in PATH.
This means that every version below this release won't have `update-self` functioning properly. I am sorry.

## [0.3.0-alpha.1] 2026-02-20

### Added
- `tags` field to the registry, which is shown in the search results and package info. This allows package authors to categorize their packages with tags, making it easier for users to find relevant packages.
- `sha256` field to the registry, which is used to verify the integrity of the downloaded package.
- `--tags` option to the `search` command, which allows users to filter search results by tags.
- `(installed)` indicator in search results, which shows which packages are already installed.
- `--detailed` option to the `search` command, which shows more detailed information about the packages in the search results, including tags.

### Changed
- Registry now has separate `description`, and `tags` fields.
- Search results now show the package description and tags (if available) in a more organized way.
- View results now show the package description and tags (if available) in a more organized way.
- You can now search for packages by tags using the `--tags` option in the `search` command.

### Deprecated
- None for now.

### Removed
- None for now.

### Fixed
- Fixed some bugs and edge cases in the codebase, and improved the overall stability and performance of the application.

### Security
- Finally added `SHA256` checksums to the registry, which allows users to verify the integrity of the downloaded packages and protect against tampering and corruption.

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
