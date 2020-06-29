import os
from io import BytesIO
import secrets
import psycopg2
from PIL import Image
from flask import (Flask, escape, request, render_template,
 					url_for, flash, redirect, abort, send_file)
from flask_sqlalchemy import SQLAlchemy
from digistore import app, db, bcrypt, mail
from digistore.models import User, Post, Category
from digistore.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from werkzeug.utils import secure_filename


UPLOAD_FOLDER='/static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'png', 'zip', 'rar', '7zip', 'mp4', 'mov',
						'wmv', 'flv', 'avi', 'eps','epsi','epsf','psd','tif',}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")



@app.route("/software")
def software():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=1).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("software.html", posts=posts)


@app.route("/webapps")
def webapps():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=2).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("webapps.html", posts=posts)


@app.route("/games")
def games():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=3).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("games.html", posts=posts)


@app.route("/movies")
def movies():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=4).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("movies.html", posts=posts)


@app.route("/ebooks")
def ebooks():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=5).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("ebooks.html", posts=posts)


@app.route("/videos")
def videos():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=6).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("videos.html", posts=posts)


@app.route("/audio_music")
def audio_music():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=7).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("audio_music.html", posts=posts)


@app.route("/photography")
def photography():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=8).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("photography.html", posts=posts)


@app.route("/GraphicDigitalArt")
def digiralart():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=9).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("digitalart.html", posts=posts)


@app.route("/documents")
def documents():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=10).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("documents.html", posts=posts)


@app.route("/courses")
def courses():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=11).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("courses.html", posts=posts)


@app.route("/proff")
def proff():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=12).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("proff.html",posts=posts)


@app.route("/tickets")
def tickets():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(category_id=13).order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template("tickets.html", posts=posts)


@app.route("/buy")
def buy():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(
	    Post.date_posted.desc()).paginate(page=page, per_page=16)
	return render_template('buy.html', posts=posts)

@app.route("/faq")
def faq():
	return render_template("faq.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(url_for('home'))# if next_page else redirect(url_for('home'))
		else:
			flash(f'Loggin Faild, Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
	              sender='noreplay@demo.com', recipients=[user.email])
	msg.body = f''' To reset your password, visit the following link:
{url_for('reset_token', token = token, _external = True)}
If You did not make this request then simpy ignore this email and no changes will be made.	
'''
	mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instruction to reset your password', 'info')
		return redirect(url_for('login'))
	return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('reset_request'))

	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated! You are now able to log in.', 'success')
		return redirect(url_for('login'))
	return render_template('reset_token.html', title='Reset Password', form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def sell_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/postimg', picture_fn)

	output_size = (225, 225)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn


def save_pitcure(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/img', picture_fn)

	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn


@app.route("/checkout/<int:post_id>", methods=['POST','GET'])
@login_required
def checkout(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template("checkout.html", title=post.title, post=post)

@app.route("/download/<int:post_id>", methods=['POST','GET'])
def download(post_id):
	p = Post.query.get_or_404(post_id)
	file_data = Post.query.filter_by(id=p).first()
	return send_file(BytesIO(file_data.file_upload), as_attachment=True, attachment_filename="TEST")
	

@app.route("/sell", methods=['GET', 'POST'])
@login_required
def sell():
	form = PostForm()
	if form.validate_on_submit():
		c = form.category.data
		if(c=="Software"):
			cid = 1
		elif (c=='WebApplications'):
			cid = 2
		elif(c=="Games"):
			cid = 3
		elif(c=="Movies"):
			cid = 4
		elif(c=="eBooks"):
			cid = 5
		elif(c=="Videos"):
			cid = 6
		elif(c=="AudioMusic"):
			cid = 7
		elif(c=="Photography"):
			cid = 8
		elif(c=="GraphicDigitalArt"):
			cid = 9
		elif(c=="DocumentsGuides"):
			cid = 10
		elif(c=="Courses"):
			cid = 11
		elif(c=="ProfessionalServices"):
			cid = 12
		elif(c=="VirtualTickets"):
			cid = 13
		
		if (form.picture.data):
			img = sell_picture(form.picture.data)
		image_post = img
		post = Post(title=form.title.data, content=form.content.data, author=current_user, category_id=cid,
					price=form.price.data, image_post=image_post, contact=form.contact.data,
					file_upload=form.file_upload.data.read())
		db.session.add(post)
		db.session.commit()
		flash('Success', 'success')
		return redirect(url_for('home'))
	return render_template('sell.html', title='Sell', form=form, legend='Продади!')


@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

@app.route("/user/<string:username>")
@login_required
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('user_post.html', posts=posts, user=user)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title='New Post', form=form, legend='New Post')



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_pitcure(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('your account has been updated', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='img/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your post has been updated!', 'success')
		return redirect(url_for('post', post_id=post.id))
		
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')
	

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted!')
	return redirect(url_for('home'))

