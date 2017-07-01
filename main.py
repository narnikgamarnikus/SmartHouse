from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from flask import session

from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import Required

import speech_recognition as sr

from main_wit import client

from text_to_speach import text_to_speach
from natural_language_understanding import nlu
import settings as s
import os
from utils import generator
from conversation import conversation
import json


class SpeachForm(FlaskForm):
    text = TextField('openid', validators = [Required()])

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def hello():
	form = SpeachForm()
	filename = ''
	if request.method == "POST":
		if form.validate_on_submit():
			filename = generator()
			#wit_response = client.message(str(form.text.data))
			c = conversation(form.text.data)
			#response = nlu(form.text.data)
			answer = json.loads(c)
			answer = answer['output']['text'][0]
			#flash('I heard you say: ' + str(form.text.data))
			#flash('Yay, got Wit.ai response: ' + str(wit_response))
			#flash('I understand: ' + response)
			#flash('Answer from bot: ' + str(c))
			flash('You: ' + str(form.text.data))
			flash('Julia: ' + str(answer))
			text_to_speach(answer, filename)
			return render_template('index.html', form=form, play=True, filename=filename)
	return render_template('index.html', form=form, play=True, filename=filename )


app.config['UPLOAD_FOLDER'] = s.UPLOAD_FOLDER
app.secret_key = s.SECRET_KEY
