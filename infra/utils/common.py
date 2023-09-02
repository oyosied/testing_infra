from pathlib import Path

import random
import string

length = random.randint(1, 15)
RANDOM_STRING = ''.join(random.choice(string.ascii_letters) for _ in range(length))


ROOT_DIR = Path(__file__).parent.parent.parent
CONFIG_FILE = 'config.json'

CHARACTER_FIELDS = ['name', 'education', 'height', 'identity', 'other_aliases', 'universe', 'weight', None]
BIG_STRING = 'testing' * 55
DATA_TYPES = [None, True, False, 42, 3.14, '3-D+Man', [1, 2], {'key': 'value'}, BIG_STRING, RANDOM_STRING]
