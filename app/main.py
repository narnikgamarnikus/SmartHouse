# FLASK IMPORTS
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from flask import session, g
#from flask_socketio import SocketIO
#######################################
# BOTS IMPORTS 
from app.bots.main_wit import client
from app.bots.natural_language_understanding import nlu
from app.bots.conversation import conversation
from app.bots.text_to_speach import text_to_speach
from app.bots.weather import weather
#######################################
# UTILS IMPORTS
from app.utils.generator import generator
#######################################
# OTHERS IMPORTS
import ujson as json
import requests
import geocoder
#######################################
# APP IMPORTS 
from .forms import SpeachForm
#######################################
import os
from .settings import SECRET_KEY, UPLOAD_FOLDER


app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def hello():
	form = SpeachForm()
	filename = ''
	if not 'context' in session:
		session['context'] = None
	if request.method == "POST":
		if form.validate_on_submit():
			filename = generator()
			question = json.loads(nlu(form.text.data))
			answer = json.loads(conversation(form.text.data, context=session['context']))
			session['context'] = answer['context']
			if answer['intents'][0]['intent'] == 'weather':
				if answer['entities']:
					#print('ENTITY IS: ' + str(answer['entities'][0]['entity']))
					#print('VALUE IS: ' + str(answer['entities'][0]['value']))
					city = answer['entities'][0]['value']
					answer = weather(city)
			else:
				answer = answer['output']['text']
			#print('INTENT IS: ' + str(answer['intents'][0]['intent']))
			#if answer['intents'][0]['intent'] = 'weather':
			#	answer = weather(question)
			#	if answer:
			#		text_to_speach(answer, filename)
			#print('INTENT CONFIDENCE IS: ' + str(answer['intents'][0]['confidence']))
			'''
			answer = weather(question)
			if answer:
				text_to_speach(answer, filename)
			else:
				answer = json.loads(conversation(form.text.data, context=session['context']))
			'''
			text_to_speach(answer, filename)
			
			return render_template('index.html', form=form, play=True, filename=filename)
	return render_template('index.html', form=form, play=True, filename=filename )


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = SECRET_KEY


