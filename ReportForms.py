from wtforms import Form, RadioField, validators, StringField


class CreateReportForm(Form):
    type = RadioField('Report Type', [validators.DataRequired()], choices=[('D', 'Daily'), ('M', 'Monthly'), ('Y', 'Yearly')], default='D')
    day = StringField("Day", [validators.Length(max=2)], render_kw={"placeholder": "DD", "type": "number", "min": "1", "max": "31"})
    month = StringField("Month", [validators.Length(max=2)], render_kw={"placeholder": "MM", "type": "number", "min": "1", "max": "12"})
    year = StringField("Year", [validators.Length(max=4), validators.DataRequired()], render_kw={"placeholder": "YYYY", "type": "number", "max": "9999"})

