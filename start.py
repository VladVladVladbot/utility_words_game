import os
import sys

from game_modes.game_irregular_verbs import generate_msg, game_irregular_verbs, CloseGame
from game_modes.game_new_words import game_new_words
from game_modes.game_settings import game_settings


def menu():
    while True:
        try:
            os.system('clear')
            print(generate_msg('Hi, choose the mode!', last_slash=True), end='')
            print(generate_msg('1. IRREGULAR VERBS | 2. NEW WORDS | 3. SETTINGS | 1/2/3 ?', last_slash=True))
            cmd = str(input('~$ '))
            try:
                if cmd == '1':
                    game_irregular_verbs()
                elif cmd == '2':
                    os.system('clear')
                    sub_cmd = str(input(generate_msg('Choose the mode! | 1. eng/ru | 2. ru/eng | 1/2 ?') + '\n~$ '))
                    if sub_cmd == '1':
                        game_new_words('eng/ru')
                    game_new_words('ru_eng')
                elif cmd == '3':
                    game_settings()
            except (KeyboardInterrupt, CloseGame):
                pass
        except KeyboardInterrupt:
            os.system('clear')
            sys.exit(3)


if __name__ == '__main__':
    menu()
