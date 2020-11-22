#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# File        : textpro.py
# Project     : udemy
# Created By  : Caue Guidotti
# Created Date: 10/25/2020
# =============================================================================
"""
On Section 8, video 61, Ardit shows a scripts called TextPro and asks us to try
to write our own version... here's mine
"""
# =============================================================================

import itertools


def is_question(phrase):
    """
    Identify if phrase is a question
    :param phrase: lower case phrase part
    :rtype: bool
    """
    # if contains question mark, it is a question, if not, identify questions by looking at the beginning of phrases
    if '?' in phrase:
        return True

    # contractions will be replaced by long form without negation
    contraction_dict = {'arent': 'are', 'cant': 'can', 'hadnt': 'had', 'wasnt': 'was', 'shouldnt': 'should',
                        'isnt': 'is', 'hasnt': 'has', 'doesnt': 'does', 'dont': 'do', 'mustnt': 'must',
                        'werent': 'were', 'wouldnt': 'would', 'didnt': 'did'}
    for contraction, expanded_form in contraction_dict.items():
        phrase = phrase.replace(contraction, expanded_form)

    # Possible style of questions below. Verb, subject and noun to be replaced later.
    raw_question_format = [
        "where {aux_verb}",
        "what {aux_verb}",
        "how {aux_verb}",
        "how {aux_noun} {aux_verb}",
        "why {aux_verb}",
        "what time",
        "who {aux_verb}",
        "when {aux_verb}",
        "can {aux_sub}",
        "could {aux_sub}",
        "should {aux_sub}",
        "may {aux_sub}",
        "will {aux_sub}",
        "am {aux_sub}",
        "do {aux_sub}",
        "does {aux_sub}",
        "had {aux_sub}",
        "must {aux_sub}",
    ]

    # auxiliary verbs/subjects/nouns
    aux_verbs = ["do", "does", "did", "are", "is", "were", "was", "have", "has", "will", "would", "could"]
    aux_subjs = ["i", "you", "he", "she", "it", "they"]
    aux_nouns = ["much", "many", "long"]

    # get all possible combinations
    question_formats = {question_style.format(aux_verb=aux_verb, aux_sub=aux_sub, aux_noun=aux_noun)
                        for question_style in raw_question_format
                        for aux_verb, aux_sub, aux_noun in itertools.product(aux_verbs, aux_subjs, aux_nouns)}

    # check if phrase beginning matches any possible question formats
    return any(phrase.startswith(question_format) for question_format in question_formats)


def fix_phrase(phrase):
    """
    I noticed that his program fix punctuation, so I'm gonna try to do that.
    Besides, I am also gonna apply .capitalize() to it
    :param phrase: lower case phrase part
    """
    # check for punctuation
    if not phrase.endswith(('.', '?', '!')):
        # if it is a question, it must contain a question Mark, else it must end with dot
        if is_question(phrase):
            if '?' not in phrase:
                phrase += '?'
        else:
            if not phrase.endswith('.'):
                phrase += '.'

    # return phrase with first word capitalized
    return phrase.capitalize()


if __name__ == '__main__':

    user_phrases = []
    while True:
        user_raw_input = input('Say something: ')
        if user_raw_input.lower() == r'\end':
            break
        user_phrases.append(fix_phrase(user_raw_input))

    print(' '.join(user_phrases))
