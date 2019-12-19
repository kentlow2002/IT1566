from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators


class CreateUserForm(Form):
    username = StringField('Username', [validators.Length(min=8,max=150), validators.DataRequired()])
    email = RadioField('Email', [validators.Length(min=1,max=150), validators.DataRequired()])
    password = SelectField('Password', [validators.Length(min=12,max=150), validators.DataRequired()])
