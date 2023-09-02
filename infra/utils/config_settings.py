import json
import os

from infra.utils.common import ROOT_DIR, CONFIG_FILE


class ConfigSettings:
    def __init__(self, api_username: str, api_password: str, log_path: str, log_level: str):
        self.api_username = api_username
        self.api_password = api_password
        self.log_path = log_path
        self.log_level = log_level

    @classmethod
    def load(cls) -> 'ConfigSettings':
        json_path = ROOT_DIR / CONFIG_FILE
        with open(json_path, 'r') as f:
            data = json.load(f)

        api_username = data.get('api_username', '')
        api_password = data.get('api_password', '')

        if not api_username or not api_password:
            raise ValueError("api_username and api_password must not be empty")

        return cls(
            api_username=api_username,
            api_password=api_password,
            log_path=data.get('log_path', ''),
            log_level=data.get('log_level', '')
        )

ConfigSettings.load()