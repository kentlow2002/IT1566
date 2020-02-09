from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField, BooleanField, SubmitField


class CreateUserForm(Form):
    username = StringField('Username', [validators.Length(min=8,max=150), validators.DataRequired()])
    type = RadioField('Account Type', choices=[('Buyer','Customer'),('Seller','Business')], default='Buyer')
    email = StringField('Email', [validators.Length(min=8,max=150), validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8,max=150), validators.DataRequired()])

class UserLogInForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField("Remember me")

class UserUpdateForm(Form):
    username = StringField('Username', [validators.Length(min=8,max=150), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=8,max=150), validators.Email(), validators.DataRequired()])
    oldPassword = PasswordField('Current Password', [validators.Length(min=8,max=150), validators.DataRequired()])
    newPassword = PasswordField('New Password', [validators.Length(min=8,max=150), validators.Optional()])
    deleteAcc = SubmitField('Delete Account')

class ForgetEmailForm(Form):
    email = StringField('Email:', [validators.Email(), validators.DataRequired()])

class ForgetPassForm(Form):
    newPasswd = PasswordField('New Password:', [validators.Length(min=8,max=150), validators.DataRequired()])
    newPasswdConf = PasswordField('Confirm your new password:', [validators.Length(min=8,max=150), validators.DataRequired()])

class ProductsSearch(Form):
    query = StringField('Search:')
