from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, IntegerField, FloatField, validators, FileField
from flask_wtf import FlaskForm


class CreateProductForm(FlaskForm):
    productName = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    productCondition = RadioField('Product Condition', choices=[('N', 'New'), ('U', 'Used')], default='N')
    productPrice = FloatField('Price', [validators.DataRequired(), validators.NumberRange(min=0, max=None, message="Please enter a valid Price")])
    productQuantity = IntegerField('Quantity', [validators.DataRequired(), validators.NumberRange(min=0, max=None, message="Please enter a valid quantity")])
    productDescription = TextAreaField('Description', [validators.Length(min=1, max=500), validators.Optional()])
    productPicture = FileField("Insert a Picture")
