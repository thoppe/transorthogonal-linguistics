import os
import flask
import json
from flask import request
from flask.ext.wtf import Form
app = flask.Flask(__name__)

import logging, sys
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

def bin_data(data, time, bins=12, max_x=1, min_x=0):
    items = []
        
    dx = (max_x-min_x)/float(bins)
    x = min_x
    
    while x <= max_x:
        block = []
        for k,loc in enumerate(time):
            if loc>=x and loc<x+dx:
                block.append(data[k])
        items.append(block)
        x += dx

    return items 
    
from wtforms import Form, TextField, validators

class WordInputForm(Form):
    msg_empty = 'Enter a word here'
    req1 = validators.Required(message=msg_empty)
    req2 = validators.Required(message=msg_empty)

    def word_in_featureset(form, field):
        msg_unknown = "Sorry! I don't know the word {}."
        word = field.data.strip()
        if not wp.validate_word(word, features):
            raise validators.ValidationError(msg_unknown.format(word))
    
    word1 = TextField('word1',[req1,word_in_featureset])
    word2 = TextField('word2',[req2,word_in_featureset])

@app.route('/', methods=['GET', 'POST'])
def font_page():

    form = WordInputForm(request.form)

    if request.method == 'POST' and form.validate():      
        req = dict(request.form)
        w1  = req["word1"][0].strip()
        w2  = req["word2"][0].strip()
    else:
        w1,w2 = "boy","man"

    word_cutoff = 30

    if form.validate():
        result = wp.transorthogonal_words(w1, w2,
                                          features,
                                          word_cutoff)
        words, distance, time = result

        # Pop off the first and last words
        #words = words[1:-1]
        #distance = distance[1:-1]
        #time = time[1:-1]
        
        word_blocks = bin_data(words, time)
        result = [', '.join(x) if x else "&nbsp;"
                  for x in word_blocks]

    else:
        result = []
        
    args = {}
    args["word1"] = w1
    args["word2"] = w2

    logging.info("WORDS: {} {}".format(w1,w2))

    args["result_list"] = result
    #args["result_list"] = zip(*map(lambda x:x.tolist(),result))
    #print args["result_list"]
    #print map(type,zip(*map(list,result))[0])
    #args["result_json"] = json.dumps(args["result_list"])

    args["form"] = form
    
    return flask.render_template('front.html',**args)


# Load the feature set
import word_path as wp
features = wp.load_features()

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    #app.debug=True
    app.run()
