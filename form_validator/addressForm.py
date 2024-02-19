from wtforms import Form, StringField, validators, IntegerField

class AddressForm(Form):
    full_name = StringField('Full Name', validators=[validators.InputRequired(), validators.length(min=2)])
    country = StringField('Country', validators=[validators.InputRequired(), validators.length(min=2)])
    state = StringField('State', validators=[validators.InputRequired(), validators.length(min=2)])
    city = StringField('City', validators=[validators.InputRequired(), validators.length(min=2)])
    zip = StringField('Zip', validators=[validators.InputRequired(), validators.length(min=2)])
    street = StringField('Street', validators=[validators.InputRequired(), validators.length(min=2)])