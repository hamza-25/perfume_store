from wtforms import Form, StringField, IntegerField, validators, PasswordField

class LoginFrom(Form):
    email = StringField('Email', validators=[validators.InputRequired(), validators.email()])
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.length(min=6, max=25)])
    