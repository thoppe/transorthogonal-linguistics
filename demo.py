import os
import flask
import json
from flask import request
from flask.ext.wtf import Form
app = flask.Flask(__name__)

import logging
import sys
import datetime
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

# Log the queries separately
F_QUERY_LOG = open("log_word_query.txt",'a')

default_w1, default_w2 = "boy","man"

_suggest_words = ["boy","man"]
_last_used_words = _suggest_words

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

def compute_results(w1,w2,result_method):
    
    word_cutoff = 35

    result = result_method(w1, w2, features,
                           word_cutoff=word_cutoff)

    words, distance, time = result
    word_blocks = bin_data(words, time)
    result = [', '.join(x) if x else "&nbsp;"
                  for x in word_blocks]

    args = {}
    args["word1"] = w1
    args["word2"] = w2
    args["result_list"] = result

    return args


def log_query(w1,w2):
    log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    log_text = "QUERY {} {} {}".format(log_time, w1, w2)
    logging.info(log_text)
    F_QUERY_LOG.write(log_text+'\n')
    F_QUERY_LOG.flush()

@app.route('/', methods=['GET','POST'])
def front_page():
    url = '/TOL/{}/{}'.format(default_w1,default_w2)
    return flask.redirect(url, code=302)

@app.route('/TOL/', methods=['GET','POST'])
def TOL_front_page():
    url = '/TOL/{}/{}'.format(default_w1,default_w2)
    return flask.redirect(url, code=302)

@app.route('/TOL_SLERP/', methods=['GET','POST'])
def TOL_SLERP_front_page():
    url = '/TOL_SLERP/{}/{}'.format(default_w1,default_w2)
    return flask.redirect(url, code=302)

@app.route('/TOL/<w1>/<w2>', methods=['GET','POST'])
def TOL_results(w1,w2):

    form = WordInputForm(request.form)
    result_method = tol.transorthogonal_words

    if request.method == 'POST' and form.validate():
        req = dict(request.form)
        w1 = req["word1"][0].strip()
        w2 = req["word2"][0].strip()

        url = '/TOL/{}/{}'.format(w1,w2)
        return flask.redirect(url, code=302)

    args = compute_results(w1,w2,result_method)
    args["form"] = form
    args["starlink"] = "TOL_SLERP"
    args["starcolor"] = "inherit"
    args["buttontext"] = "transorthogonal path"

    # Log the results!
    log_query(w1,w2)
    
    return flask.render_template('front.html', **args)

@app.route('/TOL_SLERP/<w1>/<w2>', methods=['GET','POST'])
def TOL_SLERP_results(w1,w2):

    form = WordInputForm(request.form)
    result_method = tol.slerp_word_path

    if request.method == 'POST' and form.validate():
        req = dict(request.form)
        w1 = req["word1"][0].strip()
        w2 = req["word2"][0].strip()

        url = '/TOL_SLERP/{}/{}'.format(w1,w2)
        return flask.redirect(url, code=302)

    args = compute_results(w1,w2,result_method)
    args["form"] = form

    args["starlink"] = "TOL"
    args["starcolor"] = "blue"
    args["buttontext"] = "SLERP path"

    # Log the results!
    log_query(w1,w2)
    
    return flask.render_template('front.html', **args)


# Load the feature set
import transorthogonal_linguistics as tol
features = tol.Features()

if __name__ == '__main__':
    app.debug = False
    #app.debug = True
    app.run()
