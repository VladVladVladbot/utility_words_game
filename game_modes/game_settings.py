import os
import sys
from pathlib import Path

from game_modes.game_irregular_verbs import generate_msg, update_words, get_settings
from game_modes.service_files.exceptions import ClearConsole

SETTINGS_PATH = Path(sys.path[0]) / Path('saves/irregular_words/general_settings.txt')
DEFAULT_SETTINGS = {'WORDS_PATH': '~/Desktop/MyDoc/projects/game_words/saves/irregular_words/words.txt',
                    'HISTORY_UPDATE_FREQUENCY': '1'}


def update_settings(path=SETTINGS_PATH, res=None) -> None:
    update_words(path=path, res=res)


def game_settings() -> None:
    os.system('clear')
    settings = get_settings()
    print(generate_msg('SETTINGS'))
    print(generate_msg(f'You can change {" | ".join(settings.keys())}'), end='\n\n')
    for k, v in settings.items():
        print(f'{k}={v}')
    while True:
        try:
            cmd = str(input('\n~$ '))
            if cmd == 'clear':
                raise ClearConsole
            if cmd == 'set default':
                # update_settings(path=SETTINGS_PATH, DEFAULT_SETTINGS)
                pass
            if settings.get(cmd, None):
                print(cmd, end='')
                continue
            command = cmd.split('=')
            if len(command) == 2:
                # update_settings(path=SETTINGS_PATH, )
                pass

        except ClearConsole:
            print(generate_msg('SETTINGS'))
            print(generate_msg(f'You can change {" | ".join(settings.keys())}'), end='\n\n')
            for k, v in settings.items():
                print(f'{k}={v}')
