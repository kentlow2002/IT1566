from wtforms import Form, validators, SubmitField, IntegerField



class CartUpdateForm(Form):
    quantity = IntegerField('Quantity', [validators.NumberRange(min = 1,max = 999, message = 'You have entered an invaild integer for quantity')])


