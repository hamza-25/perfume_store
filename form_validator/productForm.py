from wtforms import Form, StringField, validators, IntegerField, FloatField, FileField

class ProductForm(Form):
    title = StringField('Title', validators=[validators.InputRequired(), validators.length(min=10)])
    description = StringField('Description', validators=[validators.InputRequired(), validators.length(min=10)])
    discount_price = FloatField('Discount Price', validators=[validators.InputRequired()])
    price = FloatField('Price', validators=[validators.InputRequired()])
    quantity = IntegerField('Quantity', validators=[validators.InputRequired()])
    file = FileField('Image', validators=[validators.InputRequired()])
    category = IntegerField('Category ID', validators=[validators.InputRequired()])