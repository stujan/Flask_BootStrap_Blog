g__author__ = 'sanjay'
from datetime import datetime
from flask import render_template, redirect, url_for, request, current_app, abort, flash

from flask_login import login_user, login_required, logout_user, current_user

from . import main
from .. import db
from ..models import Post,Posttype,Project,Contacts,BackGround,Admin
from .forms import PostForm,TypeForm,ProjectForm,ContactsForm,BgForm
from flask_util_js import  FlaskUtilJs



imgurl = None

@main.route('/', methods=['GET', 'POST'])
def index():
    global  imgurl
    imgurl = Admin.query.order_by(Admin.id).first().imgurl
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    info = Posttype.query.order_by(Posttype.id).all()
    dic = {}
    for i in info:
        dic[i.id]=i.name
    return render_template('index.html', posts=posts, pagination=pagination,dict=dic,imgurl=imgurl)


@main.route('/article/<int:id>',methods=['GET','POST'])
def post(id):
    post = Post.query.get_or_404(id)
    typename = Posttype.query.get_or_404(post.type).name
    return render_template('post.html', post=post,typename=typename)

@main.route('/hidepost/<int:id>')
@login_required
def hidepost(id):
    post = Post.query.get_or_404(id)
    post.show = False
    db.session.add(post)
    return redirect(request.referrer)

@main.route('/showpost/<int:id>')
@login_required
def showpost(id):
    post = Post.query.get_or_404(id)
    post.show = True
    db.session.add(post)
    return redirect(request.referrer)




@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if not current_app:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.subheading = form.subheading.data
        post.body = form.body.data
        post.type = form.type.data
        db.session.add(post)
        flash("the post has been update")
        return redirect(url_for('.post', id=post.id))


    # form.type.choices = [[i.id,i.name]for i in Posttype.query.order_by('id')]
    form.title.data = post.title
    form.subheading.data = post.subheading
    form.body.data = post.body
    form.type.data = post.type
    return render_template('edit_post.html', form=form)



@main.route('/edittype/<int:id>', methods=['GET', 'POST'])
@login_required
def edittype(id):
    post = Posttype.query.get_or_404(id)
    if not current_app:
        abort(403)
    form = TypeForm()
    if form.validate_on_submit():
        post.name = form.type.data
        db.session.add(post)
        return redirect(url_for('.alltype'))
    # form.type.choices = [[i.id,i.name]for i in Posttype.query.order_by('id')]
    form.type.data=post.name
    return render_template('edit_type.html', form=form)


@main.route('/test')
def test():
    return render_template('test.html')

@main.route('/add', methods=['GET', 'POST'])
@login_required
def addpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data,
                    subheading=form.subheading.data,
                    body=form.body.data,
                    type=form.type.data,
                    timestamp =datetime.utcnow())
        db.session.add(post)

        flash("the post has been submitted")

        return redirect(url_for('.index'))

    return render_template('edit_post.html',form=form)

@main.route('/addtype', methods=['GET', 'POST'])
@login_required
def addtype():
    form = TypeForm()
    if form.validate_on_submit():
        info = Posttype.query.filter_by(name=form.type.data).all()
        if info:
            flash("已经存在该类型")
        else:
            type = Posttype(name=form.type.data,
                            timestamp = datetime.utcnow())
            db.session.add(type)
            return redirect(url_for('.index'))

    return render_template('edit_type.html',form=form)

@main.route('/alltype')
def alltype():
    page = request.args.get("Tpage", 1, type=int)
    pagination = Posttype.query.order_by(Posttype.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    types = pagination.items
    return render_template('allType.html', types=types, pagination=pagination,imgurl=imgurl)


@main.route('/allarticle/<int:id>', methods=['GET', 'POST'])
def allarticle(id):
    page = request.args.get("Apage", 1, type=int)

    pagination = Post.query.filter_by(type=id).order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    info = Posttype.query.order_by(Posttype.id).all()
    dic = {}
    for i in info:
        dic[i.id]=i.name
    return render_template('allArticle.html', posts=posts, pagination=pagination,dict=dic,imgurl=imgurl)



@main.route('/addproject',methods=['GET','POST'])
@login_required
def addproject():
    form = ProjectForm()
    if form.validate_on_submit():
        project= Project(name = form.name.data,
                    heading=form.heading.data,
                    body=form.body.data,
                    imgurl=form.imgurl.data,
                    timestamp =datetime.utcnow())
        db.session.add(project)

        flash("the post has been submitted")

        return redirect(url_for('.pro'))

    return render_template('edit_project.html',form=form)


@main.route('/hideproject/<int:id>')
@login_required
def hideproject(id):
    project = Project.query.get_or_404(id)
    project.show = False
    db.session.add(project)
    return redirect(request.referrer)


@main.route('/showpost/<int:id>')
@login_required
def showproject(id):
    project = Post.query.get_or_404(id)
    project.show = True
    db.session.add(project)
    return redirect(request.referrer)

@main.route('/editproject/<int:id>', methods=['GET', 'POST'])
@login_required
def editproject(id):
    project = Project.query.get_or_404(id)
    if not current_app:
        abort(403)
    form = ProjectForm()
    if form.validate_on_submit():
        project.name= form.name.data
        project.heading = form.heading.data
        project.body = form.body.data
        project.imgurl = form.imgurl.data
        db.session.add(project)
        flash("the post has been update")
        return redirect(url_for('.project', id=project.id))


    # form.type.choices = [[i.id,i.name]for i in Posttype.query.order_by('id')]
    form.name.data = project.name
    form.heading.data = project.heading
    form.body.data = project.body
    form.imgurl.data = project.imgurl
    return render_template('edit_project.html', form=form)


@main.route('/project/<int:id>',methods=['GET','POST'])
def project(id):
    project = Project.query.get_or_404(id)
    return render_template('project.html', project=project)


@main.route('/pro')
def pro():
    page = request.args.get("page", 1, type=int)
    pagination = Project.query.order_by(Project.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    projects = pagination.items
    return render_template('allproject.html', projects=projects, pagination=pagination,imgurl=imgurl)


@main.route('/contact')
def contact():
    info = Contacts.query.order_by(Contacts.id).all()
    return render_template('contact.html',info = info[0])


@main.route('/editcontact',methods=['GET','POST'])
@login_required
def editcontact():
    contact=Contacts.query.order_by(Contacts.id).first()
    if not current_app:
        abort(403)
    form = ContactsForm()
    if form.validate_on_submit():
        if not contact:
            contact = Contacts()
        contact.name = form.name.data
        contact.content = form.content.data
        contact.email = form.email.data
        contact.imgurl = form.imgurl.data
        contact.intro = form.intro.data

        db.session.add(contact)
        flash("the post has been update")
        return redirect(url_for('.contact'))


    # form.type.choices = [[i.id,i.name]for i in Posttype.query.order_by('id')]
    if contact:
        form.name.data = contact.name
        form.content.data = contact.content
        form.email.data = contact.email
        form.imgurl.data = contact.imgurl
        form.intro.data = contact.intro
    return render_template('edit_contact.html', form=form)



@main.route('/addbg', methods=['GET', 'POST'])
@login_required
def addbg():
    form = BgForm()
    if form.validate_on_submit():
        img = BackGround(imgurl = form.imgurl.data)
        db.session.add(img)
        return redirect(url_for('.viewbg'))

    return render_template('addimg.html',form=form)


@main.route('/viewbg', methods=['GET', 'POST'])
@login_required
def viewbg():
    page = request.args.get("page", 1, type=int)
    pagination = BackGround.query.order_by(BackGround.id).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    imgs = pagination.items
    return render_template('allimg.html', imgs=imgs, pagination=pagination,imgurl=imgurl)


@main.route('/setbg/<int:id>', methods=['GET', 'POST'])
@login_required
def setbg(id):
    url = BackGround.query.get_or_404(id).imgurl
    admin = Admin.query.order_by(Admin.id).first()
    admin.imgurl = url
    global imgurl
    imgurl = url
    db.session.add(admin)
    print("!23")
    return redirect(url_for('.viewbg'))


@main.route('/stuproject/tree')
def tree():
    return render_template('tree.html')


@main.route('/stuproject/sonic')
def sonic():
    return render_template('sotest.html')
