from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import Required

class SpeachForm(FlaskForm):
    text = TextField('openid', validators = [Required()])