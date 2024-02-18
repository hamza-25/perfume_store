from wtforms import Form, StringField, validators

class ProfilFrom(Form):
    first_name = StringField('First Name', validators=[validators.InputRequired(), validators.length(min=2)])
    last_name = StringField('Last Name', validators=[validators.InputRequired(), validators.length(min=2)])
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])