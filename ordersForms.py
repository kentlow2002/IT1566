from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField, BooleanField, SubmitField


class OrderUpdateForm(Form):
    addr = StringField('Address', [validators.Optional()])
    status = SelectField('Status', choices=[("Pending", "Pending"),("Shipping","Shipping"),("Delivered","Delivered"),("Cancelled","Cancelled")], default='Pending')
    desc = TextAreaField('Description', [validators.Optional()])
