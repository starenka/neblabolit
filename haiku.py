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

    matcher1, matcher2, matcher3 = Matcher(nlp.vocab), Matcher(nlp.vocab), Matcher(nlp.vocab)
    pattern1 = [{'POS':  {'IN': ['NOUN', 'ADP', 'ADJ', 'ADV']}},
                {'POS':  {'IN': ['NOUN', 'VERB']}}]
    pattern2 = [{'POS':  {'IN': ['NOUN', 'ADP', 'ADJ', 'ADV']}},
                {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
                {'POS':  {'IN': ['NOUN', 'VERB', 'ADJ', 'ADV']}}]
    pattern3 = [{'POS':  {'IN': ['NOUN', 'ADP', 'ADJ', 'ADV']}},
                {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
                {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
                {'POS':  {'IN': ['NOUN', 'VERB', 'ADJ', 'ADV']}}]

    matcher2.add('3w', None, pattern2)
    matcher1.add('2w', None, pattern1)
    matcher3.add('4w', None, pattern3)

    doc = nlp(text)

    matches1, matches2, matches3 = matcher1(doc), matcher2(doc), matcher3(doc)
    g_5, g_7 = [], []

    for match_id, start, end in matches1 + matches2 + matches3:
        span = doc[start:end]

        syl_count = 0
        for token in span:
            sc = token._.syllables_count
            if not sc:
                continue

            syl_count += sc
            if syl_count == 5:
                if span.text not in g_5:
                    g_5.append(span.text)
            if syl_count == 7:
                if span.text not in g_7:
                    g_7.append(span.text)

    return random.choice(g_5), random.choice(g_7), random.choice(g_5)
