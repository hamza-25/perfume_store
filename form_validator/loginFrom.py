from wtforms import Form, StringField, IntegerField, validators, PasswordField

class LoginFrom(Form):
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.length(min=3, max=25)])
    