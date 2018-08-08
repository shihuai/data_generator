import os, errno
import random
import re

from tqdm import tqdm
from data_generator import generate_from_tuple
from multiprocessing import Pool

def load_dict(lang):
    """
        Read the dictionnary file and returns all words in it.
    """

    lang_dict = {}
    with open(os.path.join(lang), 'r') as d:
        lines = d.readlines()
        for line in lines:
            temp = line.strip('\n').split(' ')
            lang_dict[temp[0]] = int(temp[1])

    return lang_dict


def main():
    """
        Description: Main function
    """

    # Argument parsing
    # args = parse_arguments()

    languages = ['cn', 'eng']
    first_dir = '/data/char_img/divide_result/train'
    thread_count = 4

    for language in languages:

        # Creating word list
        lang_dict = load_dict('need_generate_word_voc_{}.txt'.format(language))

        # Create font (path) list
        # fonts = load_fonts(language)

        for word, count in lang_dict.items():

            # Create the directory if it does not exist.
            try:
                output_dir = os.path.join(first_dir, word.decode('utf-8'))
                os.makedirs(output_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            if word == 'slash':
                word = '/'

            # Creating synthetic sentences (or word)
            strings = [word] * count

            string_count = len(strings)

            print ('start produce {}.'.format(word))

            p = Pool(thread_count)
            for _ in tqdm(p.imap_unordered(
                    generate_from_tuple,
                zip(
                    [i for i in range(0, string_count)],
                    strings,
                    [language] * string_count,
                    [output_dir] * string_count,
                    [32] * string_count,
                    [32] * string_count,
                    ['jpg'] * string_count,
                    [random.randrange(0, 10) for _ in range(0, string_count)],
                    [random.randint(0, 1) for _ in range(0, string_count)],
                    [3] * string_count,
                    [random.randint(0, 2) for _ in range(0, string_count)],
                    [0] * string_count,
                )
            ), total=count):
                pass
            p.terminate()

if __name__ == '__main__':
    main()
