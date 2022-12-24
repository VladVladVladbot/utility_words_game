import os
import sys
from typing import Dict, List
from random import choice
from pathlib import Path

from game_modes.service_files.exceptions import CloseGame


BASE_PATH = Path(sys.path[0]) / Path('saves') / Path('irregular_words')


def get_settings() -> Dict[str, str]:
    with open(BASE_PATH / Path('general_settings.txt'), 'r') as s_txt:
        g_dict = {g[0]: g[1] if g[1].isdigit() else g[1][1:-1] for x in s_txt.read().split('\n') if (g := x.split('='))}
        s_txt.close()
    return g_dict


s_dict = get_settings()
WORDS_PATH = p.replace('~', str(Path.home()), 1) if (p := s_dict.get('WORDS_PATH', None)) else f'{BASE_PATH}/words.txt'
HISTORY_UPDATE_FREQUENCY = int(p) if (p := s_dict.get('HISTORY_UPDATE_FREQUENCY', None)) else 1


def get_words(path=WORDS_PATH) -> Dict[str, List[str]]:
    if not Path(WORDS_PATH).is_file():
        generate_exit(msg=generate_msg(f'The file {Path(path).parts[-1]} does not exist!'))
    with open(path, 'r') as words_txt:
        if os.stat(path).st_size == 0:
            generate_exit(msg=generate_msg(f'{Path(path).parts[-1]} is empty!'))
        res = {f'word_{ind}': line.split('_') for ind, line in enumerate(words_txt.read().split('\n')) if line != '[]'}
        words_txt.close()
    return res


def update_words(path=WORDS_PATH, *, res=None) -> None:
    with open(path, 'w') as words:
        if res is None:
            words.write('')
        else:
            for index, line in enumerate(res.values()):
                s = ''
                for l_word in line:
                    s += l_word + '_'
                words.write(s[:-1] + ('' if index == len(res) - 1 else '\n'))
        words.close()


def generate_exit(*, msg='') -> None:
    os.system('clear')
    input(msg)
    raise CloseGame


def generate_msg(*args, first_slash=False, last_slash=False, status=None) -> str:
    status, input_msg = (f"status - {status} | ", f"{'—' * 14}\n| next word? |\n{'—' * 14}") if status else ('', '')
    first_slash, last_slash = ('\n' if first_slash else '', '\n' if last_slash else '')
    amount = sum(len(x) for x in args) + len(status) + len(args) + 3
    info_msg = f"\r{first_slash}{'—' * amount}\n| {status}{' '.join(args)} |\n{'—' * amount}{last_slash}"
    return info_msg + input_msg


def game_irregular_verbs() -> None:
    res = get_words()
    list_of_words = [(x, index) for index, x in enumerate(res)]
    last_choice_word = ''
    update_history_cnt = 0
    while True:
        try:
            os.system('clear')
            choice_word, index_choice_word = choice(list_of_words)
            while all((choice_word == last_choice_word, len(list_of_words) > 1)):
                choice_word, index_choice_word = choice(list_of_words)
            last_choice_word = choice_word
            w_0, w_1, w_2, cnt_3 = res[choice_word]

            try:
                word_1, word_2, *_ = input(f'{w_0}$ ').split()
            except ValueError:
                word_1, word_2 = '', ''

            if word_1 == w_1 and word_2 == w_2:
                status = "Good"

                """Words is empty"""
                if str(cnt_3) == '1':
                    res.pop(choice_word)
                    list_of_words.pop(index_choice_word)
                else:
                    res[choice_word][3] = f"{int(cnt_3) - 1}"

                update_history_cnt += 1
                if update_history_cnt % HISTORY_UPDATE_FREQUENCY == 0:
                    update_words(res=res)
            else:
                status = 'Bad'

            input(generate_msg(w_0, w_1, w_2, status=status, first_slash=True, last_slash=True))
        except IndexError:
            update_words()
            generate_exit(msg=generate_msg("The words have gone!"))
        except KeyboardInterrupt:
            update_words(res=res)
            generate_exit(msg=generate_msg(f'SCORE | {update_history_cnt}'))
