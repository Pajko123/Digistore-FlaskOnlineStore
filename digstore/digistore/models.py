from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from digistore import db, login_manager, app
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='noimage.png')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}'), '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	image_post = db.Column(db.String(20), nullable=False, default='noimage.png')
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
	content = db.Column(db.Text, nullable=False)
	contact = db.Column(db.String(30), nullable=True)
	file_upload=db.Column((db.LargeBinary),nullable=True)
	price = db.Column(db.Float, nullable=False, default=1)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', {self.file_upload},'{self.date_posted}', {self.image_post}, '{self.contact}', '{self.content}', '{self.price}', '{self.category_id}')"


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(50), nullable=False)
	posts = db.relationship('Post', backref='category')

	def __repr__(self):
		return self.category


class Cart(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	post_id=db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)