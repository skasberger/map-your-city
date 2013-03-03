from mapyourcity import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Player(db.Model):
	id = db.Column(db.String(25), primary_key=True, unique=True)
	username = db.Column(db.String(25), unique=True)
	email = db.Column(db.String(120), unique=True)
	pw_hash = db.Column(db.String(160),unique=False)
	created_at = db.Column(db.Date(), unique=False)
	last_login = db.Column(db.Date(), unique=False)
	language = db.Column(db.String(10), unique=False)
	avatar = db.Column(db.String(30), unique=False)
	color = db.Column(db.String(10), unique=False)
	region = db.Column(db.String(80), unique=False)
	country = db.Column(db.String(80), unique=False)
	osm_login = db.Column(db.String(50), unique=True)
	osm_hash = db.Column(db.String(160), unique=False)
	
	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.pw_hash = hash_password(password)
		self.created_at = datetime.now()
		self.avatar = set_avatar()
		self.color = set_color()
		self.region = set_region()
		self.language = set_language()
		self.country = get_country(region)
 
	def hash_password(self, password):
		return generate_password_hash(self)

	def set_password(self, password):
		self.pw_hash = hash_password(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

	def set_color(self, color):
		self.color = color

	def set_region(self, region):
		self.region = region 

	def get_country(self, region):
		self.country = Regions.query.filter_by(regionname = region).first()
	
	def connect_osm(self, login, password):
		self.osm_login = login
		self.osm_hash = hash_password(password)

	def set_language(self, language):
		self.language = language
	
	def set_avatar(self, avatar):
		self.avatar = avatar

	def set_username(self, username):
		self.username = username

	def set_email(self, email):
		self.email = email

	def set_last_login(self, time):
		self.last_login = time

	def __repr__(self):
		'<Player %r>' % (self.username)

class History_Scores(db.Mode):
	id = db.Column(db.String(25), primary_key=True, unique=True)
	score_id = db.Column(db.String(25), unique=False)
	session_id = db.Column(db.String(25), unique=False)
	player_id = db.Column(db.String(25), unique=False)
	timestamp = db.Column(db.Date(), unique=False)

	def __init__(self, id, score_id, session_id, player_id):
		self.id = id #wie bekomme ich einen serial hier rein mit prefix score_ ?
		self.score_id	= score_id 
		self.session_id = session_id
		self.player_id = player_id
		self.timestamp = datetime.now()

	def __repr__(self):
		'<History Scores %r>' % (self.action_id)

class History_Badges(db.Mode):
	id = db.Column(db.String(25), primary_key=True, unique=True)
	badge_id = db.Column(db.String(25), unique=False)
	session_id = db.Column(db.String(25), unique=False)
	player_id = db.Column(db.String(25), unique=False)
	timestamp = db.Column(db.Date(), unique=False)

	def __init__(self, id, badge_id, session_id, player_id):
		self.id = id #wie bekomme ich einen serial hier rein mit prefix badge_ ?
		self.badge_id	= badge_id 
		self.session_id = session_id
		self.player_id = player_id
		self.timestamp = datetime.now()

	def __repr__(self):
		'<History Badges %r>' % (self.action_id)

class History_Geoobjects(db.Mode):
	id = db.Column(db.String(25), primary_key=True, unique=True)
	session_id = db.Column(db.String(25), unique=False)
	player_id = db.Column(db.String(25), unique=False)
	timestamp = db.Column(db.Date(), unique=False)
	osm_object_id = db.Column(db.String(25), unique=False)
	geoobject_type = db.Column(db.String(50), unique=False)
	osm_object_attr = db.Column(db.String(150), unique=False)
	x_geom = db.Column(db.String(25), unique=False)
	y_geom = db.Column(db.String(25), unique=False)

	def __init__(self, id, session_id, player_id, geoobject_type, osm_object_id, osm_object_attr, x_geom, y_geom):
		self.id = id #wie bekomme ich einen serial hier rein mit prefix geo_ ?
		self.session_id = session_id
		self.player_id = player_id
		self.timestamp = datetime.now()
		self.geoobject_type = geoobject_type
		self.osm_object_id = osm_object_id
		self.osm_object_attr = osm_object_attr
		self.x_geom = x_geom
		self.y_geom = y_geom

	def __repr__(self):
		'<History Geoobjects %r>' % (self.action_id)

class History_Social(db.Mode):
	id = db.Column(db.String(25), primary_key=True, unique=True)
	session_id = db.Column(db.String(25), unique=False)
	player_id = db.Column(db.String(25), unique=False)
	timestamp = db.Column(db.Date(), unique=False)
	social_type = db.Column(db.String(50), unique=False)

	def __init__(self, id, session_id, player_id, social_type):
		self.id = id #wie bekomme ich einen serial hier rein mit prefix social_ ?
		self.session_id = session_id
		self.player_id = player_id
		self.timestamp = datetime.now()
		self.social_type = social_type
		
	def __repr__(self):
		'<History Social %r>' % (self.action_id)

class SP_Game_Info(db.Mode):
	session_id = db.Column(db.String(25), primary_key=True, unique=True)
	player_id = db.Column(db.String(25), unique=False)
	region = db.Column(db.String(25), unique=False)
	game_type = db.Column(db.String(25), unique=False)
	session_start = db.Column(db.Date(), unique=False)
	session_end = db.Column(db.Date(), unique=False)
	session_status = db.Column(db.String(20), unique=False)

	def __init__(self, session_id, player_id, region, game_type, session_start, session_end):
		self.session_id = session_id
		self.player_id = player_id
		self.region = region
		self.game_type = game_type
		self.session_start = session_start
		self.session_end = session_end
		self.session_status = get_session_status(session_id)
	
	def get_session_status(self, session_id):

	def __repr__(self):
		'<SP Game Info %r>' % (self.session_id)

class MP_Game_Info(db.Mode):
	session_id = db.Column(db.String(25), primary_key=True, unique=True)
	region = db.Column(db.String(25), unique=False)
	game_type = db.Column(db.String(25), unique=False)
	session_start = db.Column(db.Date(), unique=False)
	session_end = db.Column(db.Date(), unique=False)
	session_status = db.Column(db.String(20), unique=False)

	def __init__(self, session_id, region, game_type, session_start, session_end):
		self.session_id = session_id
		self.region = region
		self.game_type = game_type
		self.session_start = session_start
		self.session_end = session_end
		self.session_status = get_session_status(session_id)

	def get_session_status(self, session_id):

	def __repr__(self):
		'<MP Game Info %r>' % (self.session_id)

class MP_Game_Teams(db.Mode):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	session_id = db.Column(db.String(25), unique=False)
	teamname = db.Column(db.String(25), unique=False)
	color = db.Column(db.String(25), unique=False)
	
	def __init__(self, session_id, teamname, color):
		# self.id = => serial!
		self.session_id = session_id
		self.teamname = teamname
		self.color = color

	def __repr__(self):
		'<MP Game Teams %r>' % (self.id)

class MP_Game_Team_Players(db.Mode):
	team_id = db.Column(db.Integer, primary_key=True, unique=False)
	player_id = db.Column(db.String(25), unique=False)
	completed_game = db.Column(db.String(25), unique=False)
	
	def __init__(self, team_id, player_id):
		self.team_id = team_id
		self.player_id = player_id
		# get completed game

	def __repr__(self):
		'<MP Game Team Players %r>' % (self.team_id)

class Badges(db.Mode):
	badge_id = db.Column(db.String(25), primary_key=True, unique=True)
	score = db.Column(db.String(25), unique=False)
	name = db.Column(db.String(25), unique=True)
	image = db.Column(db.String(25), unique=True)
	
	def __init__(self, badge_id, score, name, image):
		self.badge_id = badge_id
		self.score = score
		self.name = name
		self.image = image

	def __repr__(self):
		'<Badges %r>' % (self.badge_id)

class Scorelist_FFA(db.Mode):
	score_id = db.Column(db.String(25), primary_key=True, unique=True)
	name = db.Column(db.String(25), unique=True)
	score = db.Column(db.Integer, unique=False)
	
	def __init__(self, score_id, name, score):
		self.score_id = score_id
		self.name = name
		self.score = score

	def __repr__(self):
		'<Scorelist_FFA %r>' % (self.score_id)

class Regions(db.Mode):
	region_short = db.Column(db.String(25), primary_key=True, unique=True)
	regionname = db.Column(db.String(120), unique=True)
	country = db.Column(db.Integer, unique=False)

	def __init__(self, regionname, region_short, country):
		self.region_short = region_short
		self.regionname = regionname
		self.country = country

	def __repr__(self):
		'<Regions %r>' % (self.region_short)

class Schedule_MOTW(db.Mode):
	week_id = db.Column(db.String(35), primary_key=True, unique=True)
	ammenity = db.Column(db.String(25), unique=False)
	time_start = db.Column(db.Date(), unique=False)
	time_end = db.Column(db.Date(), unique=False)
	area = db.Column(db.String(25), unique=False)
	
	def __init__(self, ammenity, time_start, time_end, area):
		#self. week_id  => serial!
		self.ammenity = ammenity
		self.time_start = time_start
		self.time_end = time_end
		self.area = area

	def __repr__(self):
		'<Schedule MOTW %r>' % (self.week_id)

class Ammenities(db.Mode):
	ammenity = db.Column(db.String(35), primary_key=True, unique=True)
	long_name = db.Column(db.String(50), unique=True)
	
	def __init__(self, ammenity, long_name):
		self.ammenity = ammenity
		self.long_name = long_name

	def __repr__(self):
		'<Ammenities %r>' % (self.ammenity)

