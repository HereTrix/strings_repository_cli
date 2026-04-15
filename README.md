StringsRepository CLI
========
Simple command line tool to pull changes from [string repository](https://github.com/HereTrix/strings_repository).

Overview
--------
Application utilize `strings_repository.yaml` file for configuration. It is possible to use custom environment variable to store access token or put it directly into file. Environment variable usage is highly recommended.

Installation
-------
Install via `pip install strings_repository` 

or manually clone repository and launch `pip install .`

Usage
-------

### Check version

```
strings_repository --version
strings_repository -v
```

### Initialize configuration

To create configuration file run `strings_repository init` command and follow instructions.

```
strings_repository init [FILENAME]
```

`FILENAME` is optional. If omitted, defaults to `strings_repository.yaml`.

### Pull localization files

```
strings_repository pull [FILENAME] [--bundle BUNDLE]
```

`FILENAME` is optional. If omitted, defaults to `strings_repository.yaml`.

`--bundle` / `-b` overrides the bundle version set in the config file (e.g. `v1`, `active`).

### Configuration file

Alternatively you can create `strings_repository.yaml` file manually.

Example using an environment variable for the access token (recommended):

```yaml
env_variable: ENV_VARIABLE
host: your_host
languages:
- en
path: Source
tags:
- your_tags
type: json
```

Example using a direct access token:

```yaml
api_key: your_access_token
host: your_host
languages:
- en
path: Source
tags:
- your_tags
type: json
```

Example with a bundle version:

```yaml
env_variable: ENV_VARIABLE
host: your_host
languages:
- en
bundle: active
path: Source
tags:
- your_tags
type: json
```

License
-------

**StringsRepository CLI** is released under the MIT license. See `LICENSE` for details.
