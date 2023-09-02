import random
from typing import Union, Dict

from loguru import logger

from infra.utils.common import DATA_TYPES


class Character:
    def __init__(self,
                 name: str = None,
                 education: str = None,
                 height: Union[float, int] = None,
                 identity: str = None,
                 other_aliases: str = None,
                 universe: str = None,
                 weight: Union[float, int] = None):
        self.name = name
        self.education = education
        self.height = height
        self.identity = identity
        self.other_aliases = other_aliases
        self.universe = universe
        self.weight = weight

    def __eq__(self, other):
        return self.name == getattr(other, 'name')

    @staticmethod
    def random_character():
        return Character(name=random.choice(DATA_TYPES),
                         education=random.choice(DATA_TYPES),
                         height=random.choice(DATA_TYPES),
                         identity=random.choice(DATA_TYPES),
                         other_aliases=random.choice(DATA_TYPES),
                         universe=random.choice(DATA_TYPES),
                         weight=random.choice(DATA_TYPES))

    def assert_character(self):
        missing_fields = [field for field, value in vars(self).items() if value is None]
        if missing_fields:
            logger.error(f"{self} has missing fields: {missing_fields}")
            raise KeyError(f"{self} has missing fields: {missing_fields}")
        self.assert_character_values()

    def assert_character_values(self):
        if not 1 <= len(self.universe) <= 350:
            logger.error(f"Universe - {self.universe} length must be between 1 and 350 characters")
            raise Exception(f"Universe - {self.universe} length must be between 1 and 350 characters")
        if not 1 <= len(self.identity) <= 350:
            logger.error(f"Identity - {self.identity} length must be between 1 and 350 characters")
            raise Exception(f"Identity - {self.identity} length must be between 1 and 350 characters")
        if not 1 <= len(self.other_aliases) <= 350:
            logger.error(f"Other aliases - {self.other_aliases} length must be between 1 and 350 characters")
            raise Exception(f"Other aliases - {self.other_aliases} length must be between 1 and 350 characters")

    def __str__(self):
        attributes = [f"{attr}='{getattr(self, attr)}'" for attr in vars(self)]
        return "\n".join(attributes)

    @staticmethod
    def from_dict(data: dict, skip_assertion: bool = False) -> 'Character':
        character = Character(
            name=data.get('name'),
            education=data.get('education'),
            height=data.get('height'),
            identity=data.get('identity'),
            other_aliases=data.get('other_aliases'),
            universe=data.get('universe'),
            weight=data.get('weight')
        )

        if not skip_assertion:
            character.assert_character()

        logger.debug(f"Created character \n{character}")
        return character

    def to_dict(self) -> Dict:
        return {attr: getattr(self, attr) for attr in vars(self)}
