from wtforms import Form, RadioField, validators, StringField


class CreateReportForm(Form):
    type = RadioField('Report Type', [validators.DataRequired()], choices=[('D', 'Daily (dd/mm/yyyy)'), ('M', 'Monthly (mm/yyyy)'), ('Y', 'Yearly (yyyy)')], default='D')
    date = StringField("Date", [validators.Length(min=4, max=10), validators.DataRequired()])

