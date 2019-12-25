from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField


class CreateUserForm(Form):
    username = StringField('Username', [validators.Length(min=8,max=150), validators.DataRequired()])
    type = RadioField('Account Type', choices=[('Buyer','Customer'),('Seller','Business')], default='Buyer')
    email = StringField('Email', [validators.Length(min=8,max=150), validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=12,max=150), validators.DataRequired()])

class UserLogInForm(Form):
    username = StringField('Username', [validators.Length(min=8,max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=12,max=150), validators.DataRequired()])

class UserUpdateForm(Form):
    username = StringField('Username', [validators.Length(min=8,max=150), validators.DataRequired()])
    type = RadioField('Account Type', choices=[('Buyer','Customer'),('Seller','Business')], default='Buyer')
    email = StringField('Email', [validators.Length(min=8,max=150), validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=12,max=150), validators.DataRequired()])
