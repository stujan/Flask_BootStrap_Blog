import bleach

__author__ = 'sanjay'

from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
from flask import request,url_for
from flask_login import  UserMixin

from . import  db
from . import  login_manager

class Admin(UserMixin,db.Model):
    __tablename__ ='admin'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    imgurl = db.Column(db.String(64))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

@login_manager.user_loader
def load_user(username):
    return Admin.query.get(username)



class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    title = db.Column(db.String(64))
    type = db.Column(db.Integer)
    subheading = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    show = db.Column(db.Boolean,index=True,default=True)
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p','img']
        attrs = {
            'img': ['src', 'alt']
        }
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags,  attributes=attrs,strip=True))

db.event.listen(Post.body, 'set', Post.on_changed_body)



class Posttype(db.Model):
    __tablename__ = "posttype"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Project(db.Model):
    __tablename__ = "project"

    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    heading = db.Column(db.String(64))
    imgurl = db.Column(db.String(64),index=True,default='../static/img/home-bg.jpg')
    show = db.Column(db.Boolean,index=True,default=True)
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p','img']
        attrs = {
            'img': ['src', 'alt']
        }
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=attrs,strip=True))

db.event.listen(Project.body, 'set', Project.on_changed_body)

class Contacts(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    intro = db.Column(db.Text)
    content = db.Column(db.Text)
    #content_html = db.Column(db.Text)
    imgurl = db.Column(db.String(64))
#     @staticmethod
#     def on_changed_body(target, value, oldvalue, initiator):
#         allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
#                         'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
#                         'h1', 'h2', 'h3', 'p','img']
#         attrs = {
#             'img': ['src', 'alt']
#         }
#         target.body_html = bleach.linkify(bleach.clean(
#             markdown(value, output_format='html'),
#             tags=allowed_tags, attributes=attrs,strip=True))
#
# db.event.listen(Contacts.content, 'set', Contacts.on_changed_body)


class BackGround(db.Model):
    __tablename__ = "background"
    id = db.Column(db.Integer, primary_key=True)
    imgurl = db.Column(db.String(64))
