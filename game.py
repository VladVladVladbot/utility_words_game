import os
import sys
from typing import Dict, List
from random import choice
from pathlib import Path

BASE_PATH = f'{Path.home()}/Desktop/MyDoc/projects/game_words'
BASE_WORDS_TXT_PATH = f'{BASE_PATH}/saves/words.txt'
HISTORY_UPDATE_FREQUENCY = 1


def get_words() -> Dict[str, List[str]]:
    with open(BASE_WORDS_TXT_PATH, 'r') as words_txt:
        if os.stat(BASE_WORDS_TXT_PATH).st_size == 0:
            print(generate_msg(f'{Path(BASE_WORDS_TXT_PATH).parts[-1]} is empty!'))
            sys.exit(2)
        res = {f'word_{index}': line.split('_') for index, line in enumerate(words_txt.read().split('\n'))}
        words_txt.close()
    return res


def update_words(res=None) -> None:
    with open(BASE_WORDS_TXT_PATH, 'w') as words:
        if res is None:
            words.write('')
        else:
            for index, line in enumerate(res.values()):
                s = ''
                for l_word in line:
                    s += l_word + '_'
                words.write(s[:-1] + ('' if index == len(res) - 1 else '\n'))
        words.close()


def generate_msg(*args, status=None) -> str:
    status, input_msg = (f"status - {status} | ", f"{'—' * 14}\n| next word? |\n{'—' * 14}") if status else ('', '')
    amount = sum(len(x) for x in args) + len(status) + len(args) + 3
    info_msg = f"\n{'—' * amount}\n| {status}{' '.join(args)} |\n{'—' * amount}\n"
    return info_msg + input_msg


def main() -> None:
    res = get_words()
    list_of_words = [(x, index) for index, x in enumerate(res)]
    last_choice_word = ''
    update_history_count = 0
    while True:
        try:
            os.system('clear')
            choice_word, index_random_word = choice(list_of_words)
            while all((choice_word == last_choice_word, len(list_of_words) > 1)):
                choice_word, index_random_word = choice(list_of_words)
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
                    list_of_words.pop(index_random_word)
                else:
                    res[choice_word][3] = f"{int(cnt_3) - 1}"

                update_history_count += 1
                if update_history_count % HISTORY_UPDATE_FREQUENCY == 0:
                    update_words(res)
            else:
                status = 'Bad'

            input(generate_msg(w_0, w_1, w_2, status=status))
        except IndexError:
            print(generate_msg("The words have gone!"))
            update_words()
            sys.exit(1)
        except KeyboardInterrupt:
            print(generate_msg('Thanks for playing'))
            update_words(res)
            sys.exit(3)


if __name__ == '__main__':
    main()
