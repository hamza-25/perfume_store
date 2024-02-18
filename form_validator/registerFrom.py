from wtforms import Form, StringField, IntegerField, validators, PasswordField

class RegisterFrom(Form):
    first_name = StringField('First Name', validators=[validators.InputRequired(), validators.length(min=2)])
    last_name = StringField('Last Name', validators=[validators.InputRequired(), validators.length(min=2)])
    email = StringField('Email', validators=[validators.InputRequired(), validators.email()])
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.length(min=6, max=25)])
    confirm_password = PasswordField('Confirm Password', validators=[validators.InputRequired(), validators.EqualTo('password', message='password must match')])
    