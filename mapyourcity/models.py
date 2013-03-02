from mapyourcity import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Player(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(120), unique=True)
	pw_hash = db.Column(db.String(160),unique=False)
	points = db.Column(db.Integer, unique=False)
	created_at = db.Column(db.Date(), unique=False)
	updated_at = db.Column(db.Date(), unique=False)

  	def __init__(self, name=None, email=None, password=None):
		self.name = name
		self.email = email
		self.set_password(password)
		self.created_at = datetime.now()
		self.points = 0

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

	def __repr__(self):
		'<Player %r>' % (self.name)

class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)

class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)

class POI(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	osm_id = db.Column(db.BIGINT, unique=False)
	name = db.Column(db.String(160),unique=False)
	attribute = db.Column(db.String(200),unique=False)
	edited_by = db.Column(db.Integer, unique=False)

	def __init__(self, osm_id=None, name=None, attribute=None, edited_by=None):
		self.osm_id = osm_id
		self.name = name
		self.attribute = attribute
		self.edited_by = edited_by

	def __repr__(self):
		'<Player %r>' % (self.name)