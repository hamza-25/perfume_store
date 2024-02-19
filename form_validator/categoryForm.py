from wtforms import Form, StringField, validators
class CategoryFrom(Form):
    name = StringField('Name', validators=[validators.InputRequired(), validators.length(min=2)])
    