#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# File        : my_app1.py
# Project     : udemy
# Created By  : Caue Guidotti
# Created Date: 10/29/2020
# =============================================================================
"""
This is my version of English Thesaurus
Implemented the same functionalities shown at video:
    91. Interactive English Dictionary - How The Output Will Look Like
"""
# =============================================================================

import json
from difflib import get_close_matches


_err_messages = {
    'invalid_word': "The word doesn't exist. Please double check it.",
    'invalid_input': "Your input is invalid. Please double check it."
}


def load_data(data_fpath):
    """
    Reads a json file
    To be used to load the json dictionary
    All word in the thesaurus dict will be made lower for easier matching making
    :param data_fpath: data filepath (string)
    :return: data dictionary
    """
    with open(data_fpath) as data_fid:
        dict_data = json.load(fp=data_fid)
    dict_data = {word.lower(): meaning for word, meaning in dict_data.items()}
    return dict_data


def get_closest_match(word, dict_data):
    """
    Uses difflib.get_close_matches to obtain the closest match available on thesaurus. If a match is not found,
    return None
    :param word: word to match in thesaurus dict
    :param dict_data: thesaurus data dict
    :return: a word match or None if no match is found
    """
    best_match = get_close_matches(word, dict_data, n=1, cutoff=0.8)
    # If match was found and exists on dict, returns it, else returns None
    return best_match[0] if (best_match and best_match[0] in dict_data) else None


if __name__ == '__main__':
    data_fpath = r'data\data1.json'
    dict_data = load_data(data_fpath)

    word = input('-> Enter a word: ')
    word = word.lower()
    word_match = get_closest_match(word, dict_data) if word not in dict_data else word
    print_word_meaning = word_match is not None

    if print_word_meaning and word_match != word:
        # check with user if best matched word is acceptable
        while True:
            # while True until user input is correct
            use_consolidated_word = input(f'-> Did you mean "{word_match}" instead? Enter Y if yes, or N if no: ')
            print_word_meaning = use_consolidated_word.lower()
            print_word_meaning = print_word_meaning == 'y' if print_word_meaning in ['y', 'n'] else None
            if print_word_meaning is not None:
                break
            else:
                print(_err_messages['invalid_input'])

    # print word if found in dict, or if best match is the one user desires
    if print_word_meaning:
        print(' ' + '\r\n '.join(dict_data[word_match]))
    else:
        print(_err_messages['invalid_word'])

