from infra.properites.character import Character
from infra.utils.api_handler import ApiHandler


class ApiPaths:
    GET_CHARACTERS = '/characters'
    GET_CHARACTER = '/character'
    POST_CHARACTER = '/character'
    PUT_CHARACTER = '/character'
    DELETE_CHARACTER_BY_NAME = '/character'
    RESET_COLLECTION = '/reset'


from typing import List, Dict


class CharacterApi:
    def __init__(self, api_handler: ApiHandler):
        self.api_handler = api_handler
        self.base_path = "http://rest.test.ivi.ru/v2"
        self.characters_list = []

    def get_all_characters(self, skip_assertion: bool = False) -> List[Character]:
        response = self.api_handler.send_request(url=f"{self.base_path}{ApiPaths.GET_CHARACTERS}",
                                                 method='GET')
        character_list = response['result']
        character_list = [Character.from_dict(data=data, skip_assertion=skip_assertion) for data in character_list]
        return character_list

    def get_character(self, fields_query: Dict = None) -> Character:
        response = self.api_handler.send_request(url=f"{self.base_path}{ApiPaths.GET_CHARACTER}", params=fields_query)
        return Character.from_dict(response['result'])

    def create_character(self, character: Character, skip_assertion: bool = False):
        if not skip_assertion:
            character.assert_character()
        response = self.api_handler.send_request(url=f"{self.base_path}{ApiPaths.POST_CHARACTER}",
                                                 method='POST', data=character.to_dict())
        character_from_api = self.get_character(fields_query={'name': character.name})
        assert character_from_api == character
        all_characters = self.get_all_characters(skip_assertion=True)
        assert any(char.name == character.name for char in all_characters)

        self.characters_list.append(character)
        return response

    def reset_characters(self):
        self.api_handler.send_request(url=f"{self.base_path}{ApiPaths.RESET_COLLECTION}", method='POST')

    def delete_character(self, character: Character, field_query: Dict = None, pass_on_error:bool=False):
        if field_query is None:
            field_query = {'name': character.name}
        response = self.api_handler.send_request(url=f"{self.base_path}{ApiPaths.DELETE_CHARACTER_BY_NAME}", method='DELETE',
                                      params=field_query,pass_on_error=pass_on_error)
        if not pass_on_error:
            assert character.name in response['result']
        else:
            pass
