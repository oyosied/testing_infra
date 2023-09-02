from infra.utils.api_handler import ApiHandler
from infra.utils.character_api import CharacterApi
from infra.utils.config_settings import ConfigSettings


class TestManager:
    def __init__(self):
        self.config = ConfigSettings.load()
        self.api_handler = ApiHandler(username=self.config.api_username,
                                      password=self.config.api_password)

        self.character_api = CharacterApi(api_handler=self.api_handler)
