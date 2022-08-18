from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length

import app
from app.models import Therapist

class AddClientForm(FlaskForm):
    main_first_name = StringField('שם פרטי', validators=[DataRequired()])
    main_last_name = StringField('שם משפחה', validators=[DataRequired()])
    main_id = StringField('תעודת זהות')
    main_birth_year = StringField('שנת לידה')
    main_phone = StringField('טלפון')
    main_is_dutch = SelectField('הולנדי',choices=['כן','לא'])
    main_is_davids = SelectField('מטופל ביד דוידס',choices=['כן','לא'])
    main_status = SelectField('מצב נוכחי',choices=app.Config.LIVING_STATUS)

    second_first_name = StringField('שם פרטי')
    second_last_name = StringField('שם משפחה')
    second_id = StringField('תעודת זהות')
    second_birth_year = StringField('שנת לידה')
    second_phone = StringField('טלפון')
    second_is_dutch = SelectField('הולנדי',choices=['כן','לא'])
    second_status = SelectField('מצב נוכחי',choices=app.Config.LIVING_STATUS)

    city_choice = StringField('כתובת-עיר', validators=[DataRequired()])
    street_choice = StringField('כתובת-רחוב', validators=[DataRequired()])
    # address_city = StringField('כתובת-עיר', validators=[DataRequired()])
    # address_street = StringField('כתובת-רחוב', validators=[DataRequired()])
    #
    address_house_num = StringField('כתובת-מס בית', validators=[DataRequired()])

    therapist_id = SelectField('מטפל', choices=[])
    description = TextAreaField('הערות',
                             validators=[Length(min=0, max=200)])
    submit = SubmitField('הוסף לקוח')



class EditClientForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me',
                             validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditClientForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = Therapist.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}
        super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
