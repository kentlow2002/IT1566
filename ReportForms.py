from wtforms import Form, RadioField, validators, StringField, IntegerField


class CreateReportForm(Form):
    type = RadioField('Report Type', [validators.DataRequired()], choices=[('D', 'Daily (dd/mm/yyyy)'), ('M', 'Monthly (mm/yyyy)'), ('Y', 'Yearly (yyyy)')], default='D')
    date = StringField("Date", [validators.Length(min=4, max=10), validators.DataRequired()])

class CreateReportFilter(Form):
    day = IntegerField("Day", [validators.Optional, validators.NumberRange(min=1, max=31)])
    month = IntegerField("Month", [validators.Optional, validators.NumberRange(min=1, max=12)])
    year = IntegerField("Year", [validators.Optional])
