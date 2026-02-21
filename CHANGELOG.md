# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] 2026-02-21

### Added
- `info` command, detailed package info with offline fallback mode
- `clean` command, remove orphaned binaries from the bin directory
- `changelog` command, fetches and renders CHANGELOG.md live from GitHub. Will always show the newest one, though. Will make it show that specific version in the future.
- `runner` field, lets packages specify an interpreter (sh, python, etc.), used by `run`. Will default to direct execution without an interpreter.
- `tags` field, categorization, searchable via `--tags` on the `search` command.
- `sha256` field, checksum verification with tamper detection.
- `--force` flag on `install`
- `--detailed` flag on `view`
- `(installed)` indicator in search results and `info` results
- `--tags` and `--author` mutually exclusive search flags
- `update-self` now shows progress bars for the download

### Changed
- Registry fields now has more stuff.
- Temp file moved to same directory as binary, fixing cross-device issues
- `update-self` permission check before attempting update

### Fixed
- `update-self` now functions when centipm is in PATH.
- `fetch_registry()` now throws clean `ConnectionError` with helpful messages
- `run` catches `FileNotFoundError` for missing runners
- `update-self` has proper try/except around GitHub API calls
- Some error handling I didn't mention here

### Security
- SHA256 verification on install with user prompt on failure
- `update-self` permission check before attempting update


## [0.3.0-beta.2] 2026-02-21

### *Everything on 0.3.0-beta.1, and..*

### Fixed
- A fatal bug on the packages class, causing `packages.json` to not have any entries.

## [0.3.0-beta.1] 2026-02-21

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

[0.3.0]: https://github.com/tyydev1/centipm/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/tyydev1/centipm/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/tyydev1/centipm/releases/tag/v0.1.0
