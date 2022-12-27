import os
import sys

from game_modes.game_irregular_verbs import gen_msg, game_irregular_verbs, CloseGame
from game_modes.game_new_words import game_new_words
from game_modes.game_settings import game_settings


def menu() -> None:
    while True:
        try:
            os.system('clear')
            print(gen_msg('Hi, choose the mode!', last_slash=True), end='')
            print(gen_msg('1. IRREGULAR VERBS | 2. NEW WORDS | 3. SETTINGS | 1/2/3 ?', last_slash=True))
            cmd = str(input('~$ '))
            try:
                match cmd:
                    case '1':
                        game_irregular_verbs()
                    case '2':
                        while True:
                            os.system('clear')
                            sub_cmd = str(input(gen_msg('Choose the mode! | 1. eng/ru | 2. ru/eng | 1/2 ?') + '\n~$ '))
                            if sub_cmd == '1':
                                game_new_words('eng/ru')
                            elif sub_cmd == '2':
                                game_new_words('ru/eng')
                    case '3':
                        game_settings()
            except (KeyboardInterrupt, CloseGame):
                """close game"""
        except KeyboardInterrupt:
            os.system('clear')
            sys.exit(3)


if __name__ == '__main__':
    menu()
