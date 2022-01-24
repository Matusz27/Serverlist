from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, ValidationError, IPAddress, Optional, URL, NumberRange
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from DeadMatter.models import Servers, Country








class Server_submit(FlaskForm):
    name = StringField('Server Name*', validators=[DataRequired(), Length(
        min=4, max=35)])

    server_IP = StringField(
        'Server IP*', validators=[DataRequired(), IPAddress()], render_kw={
            "placeholder": "192.168.1.1"})
    
    port = IntegerField(
        'Port', validators=[Optional(), NumberRange(max=65535)], render_kw={
            "placeholder": "00000"})

    description = TextAreaField('Description*', validators=[DataRequired(), Length(
        min=10, max=200)])

    discord = StringField('Discord Link', validators=[Optional(), URL()])

    website = StringField('Website', validators=[Optional(), URL()])

    picture = FileField('Server Picture', validators=[
                        Optional(), FileAllowed(['jpg', 'png', 'gif'])])

    country = SelectField('Server Location', choices=[(str(countries.id), str(
        countries.country_name)) for countries in Country.query.all()])

    submit = SubmitField("Submit Now")

    def validate_name(self, name):
        name = Servers.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('Name is already in use!')

    def validate_server_IP(self, server_IP):
        server_IP = Servers.query.filter_by(server_IP=server_IP.data).first()
        if server_IP:
            raise ValidationError('Server IP is already in use!')


class Server_update(FlaskForm):
    name = StringField('Server Name*', validators=[DataRequired(), Length(
        min=4, max=35)])

    server_IP = StringField(
        'Server IP*', validators=[DataRequired(), IPAddress()])
    
    port = IntegerField(
        'Port', validators=[Optional(), NumberRange(max=65535)], render_kw={
            "placeholder": "00000"})
    
    description = TextAreaField('Description*', validators=[DataRequired(), Length(
        min=10, max=200)])

    discord = StringField('Discord Link', validators=[Optional(), URL()])

    website = StringField('Website', validators=[Optional(), URL()])

    picture = FileField('Server Picture', validators=[
                        Optional(), FileAllowed(['jpg', 'png'])])

    country = SelectField('Server Location', choices=[(str(countries.id), str(
        countries.country_name)) for countries in Country.query.all()])

    submit = SubmitField("Update")

    def validate_name(self, name):
        Server_name = request.path.replace("/server/", "")
        Server_name = Server_name.replace("/update", "")
        Server_name = Servers.query.get_or_404(Server_name)
        if name.data != Server_name.name:
            name = Servers.query.filter_by(name=name.data).first()
            if name:
                raise ValidationError('Name is already in use!')

    def validate_server_IP(self, server_IP):
        name = request.path.replace("/server/", "")
        name = name.replace("/update", "")
        IP = Servers.query.get_or_404(name)
        if server_IP.data != IP.server_IP:
            server_IP = Servers.query.filter_by(
                server_IP=server_IP.data).first()
            if server_IP:
                raise ValidationError('Server IP is already in use!')
