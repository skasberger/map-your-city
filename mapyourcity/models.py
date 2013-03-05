from mapyourcity import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# COMMENTS
class SettingsPlayer(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	username = db.Column(db.String(25), unique=True)
	email = db.Column(db.String(120), unique=True)
	description = db.Column(db.String(250))
	pw_hash = db.Column(db.String(160))
	created_at = db.Column(db.Date())
	last_login = db.Column(db.Date())
	lang_short = db.Column(db.String(10))
	avatar = db.Column(db.String(30))
	color = db.Column(db.String(10))
	home_region = db.Column(db.String(80))
	actual_region = db.Column(db.String(80))
	country = db.Column(db.String(80))
	osm_login = db.Column(db.String(50), unique=True)
	osm_hash = db.Column(db.String(160))
	score = db.Column(db.Integer)
	# theme = db-Column(db.String(5))
	
	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.pw_hash = self.get_hash(password)
		self.created_at = datetime.now()
		self.last_login = datetime.now()
		self.score = 0
		# self.theme = 'b'

	def get_hash(self, password):
		return generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

	def set_avatar(self, avatar='default'):
		self.avatar = avatar

	def set_description(self, description):
		self.description = description

	def set_color(self, color):
		self.color = color

	def set_actual_region(self, actual_region):
		self.actual_region = actual_region 

	def set_home_region(self, home_region):
		self.home_region = home_region 

	def get_country(self, region):
		self.country = SettingsRegions.query.filter_by(regionname = region).first()
	
	def connect_osm(self, login, password):
		self.osm_login = login
		self.osm_hash = hash_password(password)

	def set_language(self, lang_short):
		self.lang_short = lang_short
	
	def set_username(self, username):
		self.username = username

	def set_email(self, email):
		self.email = email

	def set_last_login(self, time):
		self.last_login = time

	def __repr__(self):
		'<Player %r>' % (self.username)

# COMMENTS
class HistoryOsm(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	score = db.Column(db.Integer)
	session_id = db.Column(db.Integer)
	player_id = db.Column(db.Integer)
	timestamp = db.Column(db.Date())
	object_id = db.Column(db.String(25))
	name = db.Column(db.String(150))
	ammenity = db.Column(db.String(50))
	attribute = db.Column(db.String(150))
	x_geom = db.Column(db.String(25))
	y_geom = db.Column(db.String(25))

	def __init__(self, session_id, player_id, object_id, name, ammenity, attribute):
		self.score = 1 # set dynamically
		self.session_id = session_id
		self.player_id = player_id
		self.timestamp = datetime.now()
		self.object_id = object_id
		self.name = name
		self.ammenity = ammenity
		self.attribute = attribute

	def __repr__(self):
		'<History Geoobjects %r>' % (self.session_id)

# COMMENTS
class HistoryBadges(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	badge_id = db.Column(db.Integer)
	session_id = db.Column(db.Integer)
	player_id = db.Column(db.Integer)
	timestamp = db.Column(db.Date())

	def __init__(self, badge_id, session_id, player_id):
		self.badge_id = badge_id 
		self.session_id = session_id
		self.player_id = player_id
		self.timestamp = datetime.now()

	def __repr__(self):
		'<History Badges %r>' % (self.action_id)

# COMMENTS
class HistorySocial(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	session_id = db.Column(db.Integer)
	player_id = db.Column(db.Integer)
	timestamp = db.Column(db.Date())
	social_type = db.Column(db.String(50))

	def __init__(self, session_id, player_id, social_type):
		self.session_id = session_id
		self.player_id = player_id
		self.timestamp = datetime.now()
		self.social_type = social_type
		
	def __repr__(self):
		'<History Social %r>' % (self.action_id)

# COMMENTS
class GameSp(db.Model):
	session_id = db.Column(db.Integer, primary_key=True, unique=True)
	player_id = db.Column(db.Integer)
	region = db.Column(db.String(25))
	game_type = db.Column(db.String(25))
	session_start = db.Column(db.Date())
	session_end = db.Column(db.Date())
	session_status = db.Column(db.String(20))

	def __init__(self, player_id, region, game_type):
		self.player_id = player_id
		self.region = region
		self.game_type = game_type
		self.session_start = datetime.now()
		self.session_status = 'started'
	
	# def get_session_status(self, session_id):

	def __repr__(self):
		'<SP Game Info %r>' % (self.session_id)

# COMMENTS
class GameMp(db.Model):
	session_id = db.Column(db.Integer, primary_key=True, unique=True)
	region = db.Column(db.String(25))
	game_type = db.Column(db.String(25))
	session_start = db.Column(db.Date())
	session_end = db.Column(db.Date())
	session_status = db.Column(db.String(20))

	def __init__(self, region, game_type):
		self.region = region
		self.game_type = game_type
		self.session_start = datetime.now()
		self.session_status = 'started'

	# def get_session_status(self, session_id):

	def __repr__(self):
		'<MP Game Info %r>' % (self.session_id)

# COMMENTS
class GameMpTeams(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	teamname = db.Column(db.String(25))
	session_id = db.Column(db.Integer)
	color = db.Column(db.String(25))
	
	def __init__(self, session_id, teamname, color):
		self.session_id = session_id
		self.teamname = teamname
		self.color = color

	def __repr__(self):
		'<MP Game Teams %r>' % (self.id)

# COMMENTS
class GameMpTeamsPlayers(db.Model):
	team_id = db.Column(db.Integer, primary_key=True, unique=False)
	player_id = db.Column(db.Integer)
	completed_game = db.Column(db.String(25))
	
	def __init__(self, team_id, player_id):
		self.team_id = team_id
		self.player_id = player_id
		# get completed game

	def __repr__(self):
		'<MP Game Team Players %r>' % (self.team_id)

# COMMENTS
class SettingsBadges(db.Model):
	badge_id = db.Column(db.Integer, primary_key=True, unique=True)
	score = db.Column(db.Integer)
	name = db.Column(db.String(25), unique=True)
	image = db.Column(db.String(25), unique=True)
	
	def __init__(self, score, name, image):
		self.score = score
		self.name = name
		self.image = image

	def __repr__(self):
		'<Badges %r>' % (self.name)

# COMMENTS
class SettingsScoresFfa(db.Model):
	name = db.Column(db.String(25), primary_key=True, unique=True)
	score = db.Column(db.Integer)
	
	def __init__(self, name, score):
		self.name = name
		self.score = score

	def __repr__(self):
		'<Scorelist_FFA %r>' % (self.name)

# COMMENTS
class SettingsRegions(db.Model):
	region_short = db.Column(db.String(25), primary_key=True, unique=True)
	region_full = db.Column(db.String(120), unique=True)
	country_short = db.Column(db.String(5))
	country_full = db.Column(db.String(100))

	def __init__(self, region_short, region_full, country_full, country_short):
		self.region_short = region_short
		self.region_full = region_full
		self.country_short = country_short
		self.country_full = country_full

	def __repr__(self):
		'<Regions %r>' % (self.region_short)

# COMMENTS
class ScheduleSpMotw(db.Model):
	week_id = db.Column(db.Integer, primary_key=True, unique=True)
	ammenity = db.Column(db.String(25))
	time_start = db.Column(db.Date())
	time_end = db.Column(db.Date())
	area = db.Column(db.String(25))
	
	def __init__(self, ammenity, time_start, time_end, area):
		self.ammenity = ammenity
		self.time_start = time_start
		self.time_end = time_end
		self.area = area

	def __repr__(self):
		'<Schedule MOTW %r>' % (self.time_start)

# COMMENTS
class SettingsAmmenities(db.Model):
	ammenity = db.Column(db.String(35), primary_key=True, unique=True)
	long_name = db.Column(db.String(50), unique=True)
	
	def __init__(self, ammenity, long_name):
		self.ammenity = ammenity
		self.long_name = long_name

	def __repr__(self):
		'<Ammenities %r>' % (self.ammenity)

