__author__ = 'sanjay'

from flask import render_template,redirect,request,url_for,flash
from . import  auth
from ..models import Admin
from .forms import  LoginForm
from flask_login import  login_user,login_required,logout_user
from ..models import Posttype,Post
@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin is not  None and admin.verify_password(form.password.data):
            login_user(admin,form.remember_me.data)
            return redirect((request.args.get('next') or url_for('main.index')))
        flash('Invalid username or password')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("you have been logged out")
    return redirect(url_for("main.index"))

@auth.route('/config')
@login_required
def config():
    article_type = Posttype.query.order_by(Posttype.id).all()
    return render_template('auth/config.html',articletype=article_type)
