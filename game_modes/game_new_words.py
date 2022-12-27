import os
import sys
from pathlib import Path
from random import choice

from game_modes.game_irregular_verbs import gen_msg, gen_exit, update_words, get_words, get_settings
from game_modes.game_settings import BASE_SETTINGS_PATH

BASE_NEW_WORDS_PATH = Path(sys.path[0]) / Path('saves') / Path('new_words')
WORDS_PATH = BASE_NEW_WORDS_PATH / Path('new_words.txt')


def game_new_words(mode: str) -> None:
    settings = get_settings(path=BASE_SETTINGS_PATH)
    new_words_path = p.replace('~', str(Path.home()), 1) if (p := settings.get('NEW_WORDS_PATH', None)) else WORDS_PATH
    history_update_frequency = int(p) if (p := settings.get('HISTORY_UPDATE_FREQUENCY', None)) else 1
    """settings"""

    new_res = get_words(path=new_words_path, mode=mode)
    list_of_words = [(x, index) for index, x in enumerate(new_res)]
    last_choice_word = ''
    update_history_cnt = 0
    while True:
        try:
            os.system('clear')
            choice_word, index_choice_word = choice(list_of_words)
            while all((choice_word == last_choice_word, len(list_of_words) > 1)):
                choice_word, index_choice_word = choice(list_of_words)
            last_choice_word = choice_word
            w_0, w_1, cnt_2 = new_res[choice_word]
            try:
                word, *_ = input(f'{w_0}$ ').split()
            except ValueError:
                word = ''

            if word == w_1:
                status = "Good"

                """Words is empty"""
                if str(cnt_2) == '1':
                    new_res.pop(choice_word)
                    list_of_words.pop(index_choice_word)
                else:
                    new_res[choice_word][2] = f"{int(cnt_2) - 1}"

                update_history_cnt += 1
                if update_history_cnt % history_update_frequency == 0:
                    update_words(path=new_words_path, mode=mode, res=new_res)
            else:
                status = 'Bad'

            input(gen_msg(w_0, w_1, status=status, first_slash=True, last_slash=True))
        except KeyError:
            pass
        except IndexError:
            update_words(path=new_words_path)
            gen_exit(msg=gen_msg("The words have gone!"))
        except KeyboardInterrupt:
            update_words(path=new_words_path, mode=mode, res=new_res)
            gen_exit(msg=gen_msg(f'SCORE | {update_history_cnt}'))
