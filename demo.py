import os
import flask
import json
from flask import request
from flask.ext.wtf import Form
app = flask.Flask(__name__)

import logging
import sys
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

_suggest_words = ["boy","man"]


def bin_data(data, time, bins=12, max_x=1, min_x=0):
    items = []

    dx = (max_x - min_x) / float(bins)
    x = min_x

    while x <= max_x:
        block = []
        for k, loc in enumerate(time):
            if loc >= x and loc < x + dx:
                block.append(data[k])
        items.append(block)
        x += dx

    return items

from wtforms import Form, TextField, validators


class WordInputForm(Form):
    msg_empty = 'Enter a word here'
    #req1 = validators.Required(message=msg_empty)
    #req2 = validators.Required(message=msg_empty)
    #req1 = validators.Required(message=msg_empty)
    #req2 = validators.Required(message=msg_empty)
    
    def word_in_featureset(form, field):
        msg_unknown = 'Sorry! I don\'t know the word "{}".'
        try:
            word = field.data.strip()
        except:
            word = ""
        if word and not tol.validate_word(word, features):
            raise validators.ValidationError(msg_unknown.format(word))

    word1 = TextField('word1', [word_in_featureset,])
    word2 = TextField('word2', [word_in_featureset,])


@app.route('/', methods=['GET', 'POST'])
def front_page():

    result_method = [tol.transorthogonal_words,
                     tol.slerp_word_path][1]

    form = WordInputForm(request.form)

    if request.method == 'POST' and form.validate():
        req = dict(request.form)
        w1 = req["word1"][0].strip()
        w2 = req["word2"][0].strip()
    else:
        w1, w2 = _suggest_words

    if not w1 or not w2:
        w1, w2 = _suggest_words

    word_cutoff = 35

    if form.validate() or [w1,w2]==_suggest_words:
        result = result_method(w1, w2,
                               features,
                               word_cutoff=word_cutoff)
        
        words, distance, time = result

        word_blocks = bin_data(words, time)
        result = [', '.join(x) if x else "&nbsp;"
                  for x in word_blocks]

    else:
        result = []

    args = {}
    args["word1"] = w1
    args["word2"] = w2

    logging.info("WORDS: {} {}".format(w1, w2))

    args["result_list"] = result
    args["form"] = form

    return flask.render_template('front.html', **args)


# Load the feature set
import transorthogonal_linguistics as tol
features = tol.Features()

if __name__ == '__main__':
    app.debug = True
    app.run()
