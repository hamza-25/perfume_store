from wtforms import Form, StringField, validators, IntegerField

class CheckForm(Form):
    cash = StringField('cash on delivery', validators=[validators.InputRequired()])
    address = IntegerField('address', validators=[validators.InputRequired()])