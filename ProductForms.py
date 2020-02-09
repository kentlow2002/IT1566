from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, IntegerField, FloatField, validators, FileField, SubmitField, BooleanField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from markupsafe import Markup


class CreateProductForm(FlaskForm):
    productName = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    productCondition = RadioField('Product Condition', choices=[('N', 'New'), ('U', 'Used')], default='N')
    productPrice = FloatField('Price', [validators.DataRequired(), validators.NumberRange(min=0, max=None, message="Please enter a valid Price")])
    productQuantity = IntegerField('Quantity', [validators.DataRequired(), validators.NumberRange(min=0, max=None, message="Please enter a valid quantity")])
    productDescription = TextAreaField('Description', [validators.Length(min=1, max=500), validators.Optional()])
    productPicture = FileField(" ")

class AddCartProduct(Form):
    productId = IntegerField('productId')
    addProduct = SubmitField('Add to Cart')

class EditCartProduct(Form):
    productId = IntegerField('productId')
    productQuantity = IntegerField('Quantity:', [validators.DataRequired()])

class CheckoutForm(Form):
    firstName = StringField('First Name', [validators.DataRequired()])
    lastName = StringField('Last Name', [validators.DataRequired()])
    cardNum = IntegerField('Card Number', [validators.DataRequired(),validators.Length(min=14,max=16)])
    CVV = IntegerField('CVV', [validators.DataRequired(),validators.Length(min=3,max=4)])
    expiryMonth = IntegerField('Expiry Month', [validators.DataRequired(),validators.Length(min=2,max=2)])
    expiryYear = IntegerField('Expiry Year', [validators.DataRequired(),validators.Length(min=2,max=2)])
    shippingAddr = StringField('Shipping Address', [validators.DataRequired(),validators.Length(min=10)])
