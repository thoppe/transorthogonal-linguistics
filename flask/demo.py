import os
import flask
import json
from flask import request
from flask.ext.wtf import Form
app = flask.Flask(__name__)


# Load the feature set, but not twice on debug mode
import word_path as wp
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    features = wp.load_features()

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
def hello_world():

    form = WordInputForm(request.form)

    if request.method == 'POST' and form.validate():      
        req = dict(request.form)
        w1  = req["word1"][0]
        w2  = req["word2"][0]
    else:
        w1,w2 = "boy","man"

    word_cutoff = 25

    if form.validate():
        result = wp.transorthogonal_words(w1, w2,
                                          features,
                                          word_cutoff)
    else:
        result = []
        
    args = {}
    args["word1"] = w1
    args["word2"] = w2
    args["result_list"] = zip(*map(lambda x:x.tolist(),result))
    #print map(type,zip(*map(list,result))[0])
    #args["result_json"] = json.dumps(args["result_list"])

    args["form"] = form
    
    return flask.render_template('front.html',**args)

#@app.route('/hello')
#def hello_world2():
#    return 'SUP!'

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    
    app.debug=True
    app.run()
