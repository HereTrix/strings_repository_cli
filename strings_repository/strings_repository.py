import os
import sys
import json
import requests
import yaml
import zipfile
import tempfile

__app_name__ = "strings_repository"
__version__ = "1.0.0"

CONFIG_FILE = 'strings_repository.yaml'

HOST_KEY = "host"
API_KEY = "api_key"
API_KEY_ENV_VAR = "env_variable"
TYPE_KEY = "type"
LANGUAGES_KEY = "languages"
TAGS_KEY = "tags"
PATH_KEY = "path"
BUNDLE_KEY = "bundle"

REPO_KEY = "STRINGS_REPOSITORY_KEY"


class App:

    @classmethod
    def init_config(cls, filename, host, token, env_var, type, languages, tags, path, bundle=None):
        working_dir = os.getcwd()
        file = filename if filename else CONFIG_FILE
        config_path = os.path.join(working_dir, file)

        configuration = {
            HOST_KEY: host,
            TYPE_KEY: type,
            LANGUAGES_KEY: languages.split(','),
            TAGS_KEY: tags.split(','),
            PATH_KEY: path
        }

        if env_var:
            configuration[API_KEY_ENV_VAR] = env_var

        if token:
            configuration[API_KEY] = token

        if bundle:
            configuration[BUNDLE_KEY] = bundle

        with open(config_path, 'w') as file:
            yaml.dump(configuration, file)

    @classmethod
    def pull(cls, filename, bundle=None):
        working_dir = os.getcwd()
        file = filename if filename else CONFIG_FILE
        config_path = os.path.join(working_dir, file)
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)

        env_var = config_data.get(API_KEY_ENV_VAR)
        if env_var:
            api_key = os.environ[env_var]
        else:
            api_key = config_data[API_KEY]

        data = {
            'type': config_data[TYPE_KEY],
        }

        tags = config_data.get(TAGS_KEY)
        if tags:
            data['tags'] = tags

        langs = config_data.get(LANGUAGES_KEY)
        if langs:
            data['codes'] = langs

        bundle_version = bundle or config_data.get(BUNDLE_KEY)
        if bundle_version:
            data['bundle_version'] = bundle_version

        print('Fetching data...')

        url = config_data[HOST_KEY] + '/api/plugin/export'
        response = requests.post(
            url=url,
            data=data,
            headers={
                'Access-Token': api_key
            },
        )

        print('Unpacking...')

        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            tmp.write(response.content)
            tmp.seek(0)

            config_path = config_data[PATH_KEY]
            working_dir = os.getcwd()
            path = os.path.join(working_dir, config_path)

            unzip = zipfile.ZipFile(tmp)
            unzip.extractall(path)
            print('Completed...')

    @classmethod
    def mcp(cls, filename):
        working_dir = os.getcwd()
        file = filename if filename else CONFIG_FILE
        config_path = os.path.join(working_dir, file)
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)

        env_var = config_data.get(API_KEY_ENV_VAR)
        if env_var:
            api_key = os.environ[env_var]
        else:
            api_key = config_data[API_KEY]

        mcp_url = config_data[HOST_KEY].rstrip('/') + '/api/mcp'
        headers = {
            'Access-Token': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                message = json.loads(line)
            except json.JSONDecodeError as e:
                error = {
                    'jsonrpc': '2.0',
                    'id': None,
                    'error': {'code': -32700, 'message': f'Parse error: {e}'},
                }
                sys.stdout.write(json.dumps(error) + '\n')
                sys.stdout.flush()
                continue

            try:
                response = requests.post(mcp_url, json=message, headers=headers)
                response.raise_for_status()
                sys.stdout.write(response.text.strip() + '\n')
            except requests.HTTPError as e:
                error = {
                    'jsonrpc': '2.0',
                    'id': message.get('id'),
                    'error': {'code': -32000, 'message': f'HTTP {response.status_code}: {response.text}'},
                }
                sys.stdout.write(json.dumps(error) + '\n')
            except Exception as e:
                error = {
                    'jsonrpc': '2.0',
                    'id': message.get('id'),
                    'error': {'code': -32603, 'message': str(e)},
                }
                sys.stdout.write(json.dumps(error) + '\n')
            sys.stdout.flush()
