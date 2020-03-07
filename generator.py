# coding=utf-8
import pathlib

import markovify

HERE = pathlib.Path(__file__).parent.resolve()


def get_corpus(fname):
    with open(HERE / 'data' / fname) as fh:
        return fh.read()


def train_model(fname, state_size=2, compile=False):
    ''' State size is a number of words the probability of a next word depends on. '''

    model = markovify.Text(get_corpus(fname), state_size=state_size)
    return model if not compile else model.compile(inplace=True)


def combined_model(models, weights):
    return markovify.combine(models, weights)


def generate(model, items=15, max_chars=None, separator='\n', tries=30):
    ''' By default, the make_sentence method tries a maximum of 10 times per invocation, 
    to make a sentence that does not overlap too much with the original text. 
    If it is successful, the method returns the sentence as a string. If not, it returns '''

    func, args, kwargs = model.make_sentence, [], {'tries': tries}
    if max_chars:
        func, args, kwargs = model.make_short_sentence, [max_chars], {}

    return separator.join(filter(None, [func(*args, **kwargs) for _ in range(items)]))
