import os
import sys
from typing import Dict, List
from random import choice
from pathlib import Path

from game_modes.service_files.exceptions import CloseGame


BASE_PATH = Path(sys.path[0]) / Path('saves') / Path('irregular_words')
BASE_WORDS_PATH = f'{BASE_PATH}/words.txt'
BASE_SETTINGS_PATH = Path(sys.path[0]) / Path('saves/irregular_words/general_settings.txt')


def get_settings(*, path: str | Path) -> Dict[str, str]:
    with open(path, 'r') as settings_txt:
        settings_dict = {g[0]: g[1] for x in settings_txt.read().split('\n') if (g := x.split('=')) and x}
        settings_txt.close()
    return settings_dict


def get_words(*, path: str | Path, mode: str | None = None) -> Dict[str, List[str]]:
    if not Path(path).is_file():
        gen_exit(msg=gen_msg(f'The file {Path(path).parts[-1]} does not exist!'))
    with open(path, 'r') as words_txt:
        if os.stat(path).st_size == 0:
            gen_exit(msg=gen_msg(f'{Path(path).parts[-1]} is empty!'))
        res = {f'word_{ind}': line.split('_') for ind, line in enumerate(words_txt.read().split('\n')) if line != '[]'}
        words_txt.close()
    return res if (mode != 'ru/eng') else {k: [v[1], v[0], v[2]] for k, v in res.items()}


def update_words(*, path: str | Path, mode: str | None = None, res: Dict[str, List[str]] | None = None) -> None:
    res = res if (mode != 'ru/eng') else {k: [v[1], v[0], v[2]] for k, v in res.items()}
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


def gen_exit(*, msg: str = None) -> None:
    os.system('clear')
    input(msg if msg else '')
    raise CloseGame


def gen_msg(*args, first_dash=True, last_dash=True, first_slash=False, last_slash=False, quan=None, status=None) -> str:
    status, input_msg = (f"status - {status} | ", f"{'—' * 14}\n| next word? |\n{'—' * 14}") if status else ('', '')
    """For game"""

    first_slash, last_slash = (('\n' if first_slash else ''), ('\n' if last_slash else ''))
    first_dash, last_dash = ((1 if first_dash else 0), (1 if last_dash else 0))
    mid_fs, mid_ls = (('\n' if first_dash else ''), ('\n' if last_dash else ''))
    """slashes and dashes"""

    quantity = quan if quan else sum(len(x) for x in args) + len(status) + len(args) + len(mid_fs) + len(mid_ls) + 1
    scape = (quantity - sum(len(x) for x in args) - len(status) - len(args) - 3) * ' '
    """quantity '_' and scape for custom quantity"""

    first_part = f"{first_slash}{'—' * quantity * first_dash}{mid_fs}"
    last_pard = f"{mid_ls}{'—' * quantity * last_dash}{last_slash}"
    info_msg = f"\r{first_part}| {status}{' '.join(args)}{scape} |{last_pard}"
    return info_msg + input_msg


def game_irregular_verbs() -> None:
    settings = get_settings(path=BASE_SETTINGS_PATH)
    words_path = p.replace('~', str(Path.home()), 1) if (p := settings.get('WORDS_PATH', None)) else BASE_WORDS_PATH
    history_update_frequency = int(p) if (p := settings.get('HISTORY_UPDATE_FREQUENCY', None)) else 1
    """settings"""

    res = get_words(path=words_path)
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
                if update_history_cnt % history_update_frequency == 0:
                    update_words(path=words_path, res=res)
            else:
                status = 'Bad'

            input(gen_msg(w_0, w_1, w_2, status=status, first_slash=True, last_slash=True))
        except KeyError:
            pass
        except IndexError:
            update_words(path=words_path)
            gen_exit(msg=gen_msg("The words have gone!"))
        except KeyboardInterrupt:
            update_words(path=words_path, res=res)
            gen_exit(msg=gen_msg(f'SCORE | {update_history_cnt}'))
