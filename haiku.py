# coding=utf-8

import random

from spacy.matcher import Matcher
import spacy_udpipe
from spacy_syllables import SpacySyllables


def _init(lang='cs', download_model=None):
    # ('cs', 'cs-pdt', 'cs-cac', 'cs-fictree', 'cs-cltt'):
    if download_model:
        spacy_udpipe.download(download_model)
    nlp = spacy_udpipe.load(lang)
    syllables = SpacySyllables(nlp, lang=lang)
    nlp.add_pipe(syllables)
    return nlp


def haiku(text, nlp=None):
    nlp = nlp or _init()

    m1, m2, m3 = Matcher(nlp.vocab), Matcher(nlp.vocab), Matcher(nlp.vocab)
    pattern1 = [{'POS':  {'IN': ['NOUN', 'ADP', 'ADJ', 'ADV']}},
                {'POS':  {'IN': ['NOUN', 'VERB']}}]
    pattern2 = [{'POS':  {'IN': ['NOUN', 'ADP', 'ADJ', 'ADV']}},
                {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
                {'POS':  {'IN': ['NOUN', 'VERB', 'ADJ', 'ADV']}}]
    pattern3 = [{'POS':  {'IN': ['NOUN', 'ADP', 'ADJ', 'ADV']}},
                {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
                {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
                {'POS':  {'IN': ['NOUN', 'VERB', 'ADJ', 'ADV']}}]

    m1.add('2w', None, pattern1)
    m2.add('3w', None, pattern2)
    m3.add('4w', None, pattern3)

    doc = nlp(text)
    matches = m1(doc) + m2(doc) + m3(doc)

    s5, s7 = set(), set()
    for mid, mstart, mend in matches:
        # "group of words" matching any of the patterns
        span = doc[mstart:mend]

        # get count of syllables for the whole span
        # if we can't caount the syllables, skip
        syl_count = sum(t._syllables_count or 100 for t in span)
        if syl_count == 5:
            s5.add(span.text)
        elif syl_count == 7:
            s7.add(span.text)

    s5, s7 = tuple(s5), tuple(s7)

    # haiku is 17 sylls, 5-7-5, words or lines can repeat
    return random.choice(s5), random.choice(s7), random.choice(s5)
