import pytest
from loguru import logger
from requests import HTTPError

from infra.managers.test_manager import TestManager
from infra.utils.character_api import Character
from infra.utils.common import CHARACTER_FIELDS, DATA_TYPES

"""
I assume here that /characters and /character return the value of character
from the same data source, in case it is different data source such as different DB for each
then I need to test that all characters in /characters will have a result from /character.
"""


class CharacterSuite:

    def test_all_characters(self, test_manager: TestManager):
        test_manager.character_api.get_all_characters()

    @pytest.mark.parametrize('field', CHARACTER_FIELDS)
    @pytest.mark.parametrize('data_type', DATA_TYPES)
    def test_all_fields_get_character(self, test_manager: TestManager, field, data_type):
        test_manager.character_api.get_character(fields_query={field: data_type})

    def test_create_character_random(self, test_manager: TestManager):
        character = Character.random_character()
        test_manager.character_api.create_character(character=character, skip_assertion=True)

    def test_create_character(self, test_manager: TestManager):
        character = Character(
            name="John",
            education="PhD",
            height=5.9,
            identity="secret",
            other_aliases="alias",
            universe="Marvel",
            weight=160
        )
        test_manager.character_api.create_character(character=character, skip_assertion=True)


    def test_create_character_max(self, test_manager: TestManager):
        try:
            for i in range(501):
                character = Character(
                    name=f"John{i}",
                    education="PhD",
                    height=5.9,
                    identity="secret",
                    other_aliases="alias",
                    universe="Marvel",
                    weight=160
                )
                test_manager.character_api.create_character(character=character, skip_assertion=True)
        except HTTPError as err:
            if err.response.status_code == 400 and b'{"error":"Collection can\'t contain more than 500 items"}\n' in err.response.content:
                logger.error(f"{err}")
                pass

    def test_delete_character(self, test_manager: TestManager):
        character = Character(
            name="John1",
            education="PhD",
            height=5.9,
            identity="secret",
            other_aliases="alias",
            universe="Marvel",
            weight=160
        )
        test_manager.character_api.create_character(character=character)
        test_manager.character_api.delete_character(character=character)

        test_manager.character_api.delete_character(character=character,pass_on_error=True)

