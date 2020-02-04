#python -m pip  install (for me only)
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField, BooleanField, SubmitField


class CreateStaffForm(Form):
    username = StringField('Username', [validators.Length(min=8,max=150), validators.DataRequired()])
    type = 'Staff'
    email = StringField('Email', [validators.Length(min=8,max=150), validators.Email(), validators.DataRequired()])
    newPassword = PasswordField('Password', [validators.Length(min=12,max=150), validators.DataRequired()])

class StaffUpdateForm(Form):
    username = StringField('Username', [validators.Length(min=8,max=150), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=8,max=150), validators.Email(), validators.DataRequired()])
    password = PasswordField('New Password', [validators.Length(min=12,max=150), validators.Optional()])
#{Admin}matthias
#helpmeplease
#matthiasb
#helpmeplease
#matthiass
#helpmeplease
class FaqForm(Form):
    answer = StringField('Answer', [validators.Length(min=1,max=150), validators.DataRequired()])
    question = StringField('Question', [validators.Length(min=1,max=150), validators.DataRequired()])
