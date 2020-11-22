#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# File        : my_app1.py
# Project     : udemy
# Created By  : Caue Guidotti
# Created Date: 10/29/2020
# =============================================================================
"""
This is an improved version of my_app1 (section 13) - English Thesaurus
Using mysql connector shown on section 14
"""
# =============================================================================

from python_mega_course.section13.my_app1 import get_closest_match
from python_mega_course.section14.source import get_mysql_con


_err_messages = {
    'invalid_word': "The word doesn't exist. Please double check it.",
    'invalid_input': "Your input is invalid. Please double check it."
}


def get_expressions_db(cur):
    """
    get all expressions from Dictionary table
    :param cur: an mysql.connector.cursor
    :return:
    """
    cur.execute("SELECT Expression FROM Dictionary")
    return {exp[0] for exp in cur.fetchall()}


def get_definition_db(expression, cur):
    """
    get an expression definition looking on db thesaurus
    :param expression: expression to look into db
    :param cur: an mysql.connector.cursor
    :return:
    """
    cur.execute(f"SELECT Definition FROM Dictionary WHERE Expression = '{expression}'")
    db_resp = cur.fetchall()
    return {exp[0] for exp in db_resp} if db_resp else None


if __name__ == '__main__':

    mysql_con = get_mysql_con()
    mysql_cursor = mysql_con.cursor()
    expressions_set = get_expressions_db(mysql_cursor)

    while True:
        word = input('-> Enter a word: ')
        word = word.lower()
        word_match = get_closest_match(word, expressions_set) if word not in expressions_set else word
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
            print(' ' + '\r\n '.join(get_definition_db(word_match, mysql_cursor)))
        else:
            print(_err_messages['invalid_word'])
