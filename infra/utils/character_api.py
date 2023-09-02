from loguru import logger

from infra.utils.api_handler import ApiHandler

CHARACTER_REQUIRED_FIELDS = ['name', 'education', 'height', 'identity', 'other_aliases', 'universe', 'weight']


class ApiPaths:
    GET_CHARACTERS = '/characters'
    GET_CHARACTER = '/character'
    POST_CHARACTER = '/character'
    PUT_CHARACTER = '/character'
    DELETE_CHARACTER_BY_NAME = '/character?name={name}'
    RESET_COLLECTION = '/reset'


from typing import Any, List, Dict


class Character:
    def __init__(self,
                 name: str,
                 education: str,
                 height: float,
                 identity: str,
                 other_aliases: str,
                 universe: str,
                 weight: float):
        self.name: str = name
        self.education: str = education
        self.height: float = height
        self.identity: str = identity
        self.other_aliases: str = other_aliases
        self.universe: str = universe
        self.weight: float = weight

    def __str__(self):
        attributes = [f"{attr}='{getattr(self, attr)}'" for attr in vars(self)]
        return "\n".join(attributes)

    @staticmethod
    def from_dict(data: dict) -> 'Character':
        missing_fields = []
        for field in CHARACTER_REQUIRED_FIELDS:
            if field not in data:
                missing_fields.append(field)
        if missing_fields:
            logger.error(f"Data - {data} \n Missing fields: {missing_fields}")
            raise KeyError(f"Data - {data} \n Missing fields: '{missing_fields}'")

        character = Character(
            name=data['name'],
            education=data['education'],
            height=data['height'],
            identity=data['identity'],
            other_aliases=data['other_aliases'],
            universe=data['universe'],
            weight=data['weight']
        )

        logger.debug(f"Created character \n{character}")
        return character


class CharacterApi:
    def __init__(self, api_handler: ApiHandler):
        self.api_handler = api_handler
        self.base_path = "http://rest.test.ivi.ru/v2"

    def get_all_characters(self) -> List[Character]:
        response = self.api_handler.send_request(url=f"{self.base_path}{ApiPaths.GET_CHARACTERS}",
                                                 method='GET')
        character_list = response['result']
        character_list = [Character.from_dict(data) for data in character_list]
        return character_list
