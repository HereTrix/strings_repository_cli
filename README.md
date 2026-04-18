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

### MCP proxy (stdio)

The CLI can act as a stdio MCP proxy, forwarding JSON-RPC messages to the server's `/api/mcp` endpoint. This lets IDEs and AI agents that only support stdio MCP transport (e.g. Claude Code, Cursor) use StringsRepository tools without direct HTTP access.

```
strings_repository mcp [FILENAME]
```

`FILENAME` is optional. If omitted, defaults to `strings_repository.yaml`. Use it to select a specific project configuration:

```
strings_repository mcp my-project.yaml
```

#### Claude Code setup

Add the following to your Claude Code MCP configuration (`.claude/mcp.json` or user-level `~/.claude/mcp.json`):

```json
{
  "mcpServers": {
    "strings-repository": {
      "type": "stdio",
      "command": "strings_repository",
      "args": ["mcp"]
    }
  }
}
```

To use a custom config file (e.g. for a specific project):

```json
{
  "mcpServers": {
    "strings-repository": {
      "type": "stdio",
      "command": "strings_repository",
      "args": ["mcp", "my-project.yaml"]
    }
  }
}
```

The proxy uses the same `host` and access token (`api_key` / `env_variable`) from the config file. Make sure the config points to a server that exposes the `/api/mcp` endpoint.

#### Available MCP tools

| Tool | Description |
| ---- | ----------- |
| `get_project` | Get project info for the configured token |
| `get_languages` | List all configured language codes |
| `list_tokens` | List/search localization keys |
| `get_token` | Get a key with all its translations |
| `create_token` | Create a new localization key |
| `set_translation` | Create or update a translation |
| `search_similar_tokens` | Find keys similar to a given text |
| `suggest_token_key` | Suggest a key name from source text |
| `get_token_naming_patterns` | Analyze the project's key naming conventions |
| `batch_create_tokens` | Create multiple keys with translations in one call |

License
-------

**StringsRepository CLI** is released under the MIT license. See `LICENSE` for details.
