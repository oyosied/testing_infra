from infra.managers.test_manager import TestManager


class CharacterSuite:

    def test_all_characters(self, test_manager: TestManager):
        test_manager.character_api.get_all_characters()
