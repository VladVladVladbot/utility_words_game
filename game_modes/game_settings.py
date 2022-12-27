import os
import sys
from pathlib import Path
from typing import Dict, Tuple

from game_modes.game_irregular_verbs import gen_msg, get_settings

BASE_SETTINGS_PATH = Path(sys.path[0]) / Path('saves/irregular_words/general_settings.txt')
SETTINGS_VAR_TABLE_LENGTH = 40
DEFAULT_SETTINGS = {
    'WORDS_PATH': '~/Desktop/MyDoc/projects/game_words/saves/irregular_words/words.txt',
    'NEW_WORDS_PATH': '~/Desktop/MyDoc/projects/game_words/saves/new_words/new_words.txt',
    'HISTORY_UPDATE_FREQUENCY': '1'
}


def update_settings(path: str | Path = BASE_SETTINGS_PATH, *, settings: Dict[str, str] | None = None) -> None:
    with open(path, 'w') as words:
        if settings is None:
            words.write('')
        else:
            for index, k_v in enumerate(settings.items()):
                words.write(f"{k_v[0]}={k_v[1]}" + ('' if index == len(settings) - 1 else '\n'))
        words.close()


def clear_console(settings: Dict[str, str], commands: Tuple[str, ...], v_len: int = SETTINGS_VAR_TABLE_LENGTH) -> None:
    os.system('clear')
    print(gen_msg(f'SETTINGS'))
    print(gen_msg(f'COMMANDS | {" | ".join(commands)}'))
    print(gen_msg('VARIABLES', last_dash=False, quan=v_len))
    for index, key in enumerate(settings.keys()):
        if index == 0:
            print(gen_msg(key, last_dash=False, quan=v_len))
        elif index == len(settings.keys()) - 1:
            print(gen_msg(key, first_dash=False, quan=v_len), end='\n\n')
        else:
            print(gen_msg(key, last_dash=False, first_dash=False, quan=v_len))


def game_settings() -> None:
    settings = get_settings(path=BASE_SETTINGS_PATH)
    commands = ("help", "vars", "cat", "clear", "set default", "variable=value")
    clear_console(settings=settings, commands=commands)
    while True:
        settings = get_settings(path=BASE_SETTINGS_PATH)
        cmd = str(input('~$ '))

        """commands without args"""
        def clear_console_cmd() -> None: clear_console(settings=settings, commands=commands)
        def help_cmd() -> None: print('__doc__')
        def vars_cmd() -> None: print("\n".join(f'{v}={k}' for v, k in settings.items()))
        def update_settings_cmd() -> None: update_settings(path=BASE_SETTINGS_PATH, settings=DEFAULT_SETTINGS)

        dict_cmd = {'clear': clear_console_cmd, 'help': help_cmd, 'vars': vars_cmd, 'set default': update_settings_cmd}
        if prepared_cmd := dict_cmd.get(cmd, None):
            prepared_cmd()
        elif var := settings.get(cmd, None):
            print(var)
        elif len(new_vars := cmd.split('=')) == 2 and new_vars[0] in settings.keys():
            settings.update({new_vars[0]: new_vars[1]})
            update_settings(path=BASE_SETTINGS_PATH, settings=settings)
        elif (p := cmd.split()) and p[0] == 'cat':
            print(os.system(f'cat {p[1]}') if len(p) == 2 else 'command cat has 1 arg')
        else:
            print('' if not cmd else f'{cmd} command not found\n', end='')
