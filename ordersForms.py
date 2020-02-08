from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField, BooleanField, SubmitField


class OrderUpdateForm(Form):
    addr = StringField('Address', [validators.Length(min=8,max=150), validators.Optional()])
    status = SelectField('Status', choices=[("Pending, Pending"),("Shipping,Shipping"),("Delivered","Delivered"),("Cancelled","Cancelled")])
