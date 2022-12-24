import os
import sys
from pathlib import Path
from random import choice

from game_modes.game_irregular_verbs import generate_msg, generate_exit, update_words, HISTORY_UPDATE_FREQUENCY, \
    get_words

BASE_NEW_WORDS_PATH = Path(sys.path[0]) / Path('saves') / Path('new_words')
NEW_WORDS_PATH = str(BASE_NEW_WORDS_PATH / Path('new_words.txt'))


def game_new_words(mode) -> None:
    _res = get_words(path=NEW_WORDS_PATH)  # 1
    new_res = _res if mode == 'eng/ru' else {x: [y[1], y[0], y[2]] for x, y in _res.items()}  # 2
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
            w_0, w_1, cnt_2 = new_res[choice_word]  # 3

            try:
                word, *_ = input(f'{w_0}$ ').split()  # 4
            except ValueError:
                word = ''

            if word == w_1:  # 5
                status = "Good"

                """Words is empty"""
                if str(cnt_2) == '1':  # 6
                    new_res.pop(choice_word)
                    list_of_words.pop(index_choice_word)
                else:
                    new_res[choice_word][2] = f"{int(cnt_2) - 1}"  # 7

                update_history_cnt += 1
                if update_history_cnt % HISTORY_UPDATE_FREQUENCY == 0:
                    update_words(path=NEW_WORDS_PATH, res=new_res)
            else:
                status = 'Bad'

            input(generate_msg(w_0, w_1, status=status, first_slash=True, last_slash=True))  # 8
        except IndexError:
            update_words()
            generate_exit(msg=generate_msg("The words have gone!"))
        except KeyboardInterrupt:
            update_words(res=new_res)
            generate_exit(msg=generate_msg(f'SCORE | {update_history_cnt}'))
