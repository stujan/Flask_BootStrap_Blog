__author__ = 'sanjay'

from flask_wtf import  Form
from wtforms import TextAreaField,SubmitField,StringField,SelectField
from wtforms.validators import  DataRequired,Required
from flask_pagedown.fields import  PageDownField
from ..models import Posttype
class PostForm(Form):
    title = StringField(validators=[Required()])
    type = SelectField('Article Type',coerce=int)
    subheading = StringField(validators=[Required()])
    body = PageDownField(validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(PostForm,self).__init__(*args, **kwargs)
        self.type.choices = [(type.id,type.name) for type in Posttype.query.order_by(Posttype.name).all()]


class TypeForm(Form):
    type =StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')


class ProjectForm(Form):
    name = StringField(validators=[DataRequired()])
    body = PageDownField(validators=[DataRequired()])
    heading = StringField(validators=[DataRequired()])
    imgurl = StringField()
    submit = SubmitField('Submit')


class ContactsForm(Form):
    name = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    imgurl = StringField(validators=[DataRequired()])
    intro = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')

class BgForm(Form):
    imgurl = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')
