from mapyourcity import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# COMMENTS
class SettingsPlayer(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	username = db.Column(db.String(25), unique=True)
	email = db.Column(db.String(120), unique=True)
	pw_hash = db.Column(db.String(160))
	created_at = db.Column(db.Date())
	last_login = db.Column(db.Date())
	language = db.Column(db.String(10))
	avatar = db.Column(db.String(30))
	color = db.Column(db.String(10))
	region = db.Column(db.String(80))
	country = db.Column(db.String(80))
	osm_login = db.Column(db.String(50), unique=True)
	osm_hash = db.Column(db.String(160))
	
	def __init__(self, username, email, password):
		self.id = 1
		self.username = username
		self.email = email
		self.pw_hash = self.get_hash(password)
		self.created_at = datetime.now()
		self.last_login = datetime.now()
		self.avatar = 'default'
		self.color = 'ffffff'
		self.region = 'graz'
		self.language = 'de'
		self.country = 'at'
		self.osm_login = 'openstreetmap'
		self.osm_hash = self.get_hash('hello')
 
	def get_hash(self, password):
		return generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

	def set_avatar(self, avatar='default'):
		self.avatar = avatar

	def set_color(self, color):
		self.color = color

	def set_region(self, region):
		self.region = region 

	def get_country(self, region):
		self.country = SettingsRegions.query.filter_by(regionname = region).first()
	
	def connect_osm(self, login, password):
		self.osm_login = login
		self.osm_hash = hash_password(password)

	def set_language(self, language):
		self.language = language
	
	def set_username(self, username):
		self.username = username

	def set_email(self, email):
		self.email = email

	def set_last_login(self, time):
		self.last_login = time

	def __repr__(self):
		'<Player %r>' % (self.username)

class HistoryScores(db.Model):
	id = db.Column(db.String(25), primary_key=True, unique=True)
	score_id = db.Column(db.String(25))
	session_id = db.Column(db.String(25))
	player_id = db.Column(db.String(25))
	timestamp = db.Column(db.Date())

	def __init__(self, id, score_id, session_id, player_id):
		self.id = id #wie bekomme ich einen serial hier rein mit prefix score_ ?
		self.score_id = score_id 
		self.session_id = session_id
		self.player_id = player_id
		self.timestamp = datetime.now()

	def __repr__(self):
		'<History Scores %r>' % (self.action_id)

# COMMENTS
class HistoryBadges(db.Model):
	id = db.Column(db.String(25), primary_key=True, unique=True)
	badge_id = db.Column(db.String(25))
	session_id = db.Column(db.String(25))
	player_id = db.Column(db.String(25))
	timestamp = db.Column(db.Date())

	def __init__(self, id, badge_id, session_id, player_id):
		self.id = id #wie bekomme ich einen serial hier rein mit prefix badge_ ?
		self.badge_id = badge_id 
		self.session_id = session_id
		self.player_id = player_id
		self.timestamp = datetime.now()

	def __repr__(self):
		'<History Badges %r>' % (self.action_id)

# COMMENTS
class HistoryGeo(db.Model):
	id = db.Column(db.String(25), primary_key=True, unique=True)
	session_id = db.Column(db.String(25))
	player_id = db.Column(db.String(25))
	timestamp = db.Column(db.Date())
	osm_object_id = db.Column(db.String(25))
	geoobject_type = db.Column(db.String(50))
	osm_object_attr = db.Column(db.String(150))
	x_geom = db.Column(db.String(25))
	y_geom = db.Column(db.String(25))

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

# COMMENTS
class HistorySocial(db.Model):
	id = db.Column(db.String(25), primary_key=True, unique=True)
	session_id = db.Column(db.String(25))
	player_id = db.Column(db.String(25))
	timestamp = db.Column(db.Date())
	social_type = db.Column(db.String(50))

	def __init__(self, id, session_id, player_id, social_type):
		self.id = id #wie bekomme ich einen serial hier rein mit prefix social_ ?
		self.session_id = session_id
		self.player_id = player_id
		self.timestamp = datetime.now()
		self.social_type = social_type
		
	def __repr__(self):
		'<History Social %r>' % (self.action_id)

# COMMENTS
class GameSp(db.Model):
	session_id = db.Column(db.String(25), primary_key=True, unique=True)
	player_id = db.Column(db.String(25))
	region = db.Column(db.String(25))
	game_type = db.Column(db.String(25))
	session_start = db.Column(db.Date())
	session_end = db.Column(db.Date())
	session_status = db.Column(db.String(20))

	def __init__(self, session_id, player_id, region, game_type, session_start, session_end):
		self.session_id = session_id
		self.player_id = player_id
		self.region = region
		self.game_type = game_type
		self.session_start = session_start
		self.session_end = session_end
		self.session_status = get_session_status(session_id)
	
	# def get_session_status(self, session_id):

	def __repr__(self):
		'<SP Game Info %r>' % (self.session_id)

# COMMENTS
class GameMp(db.Model):
	session_id = db.Column(db.String(25), primary_key=True, unique=True)
	region = db.Column(db.String(25))
	game_type = db.Column(db.String(25))
	session_start = db.Column(db.Date())
	session_end = db.Column(db.Date())
	session_status = db.Column(db.String(20))

	def __init__(self, session_id, region, game_type, session_start, session_end):
		self.session_id = session_id
		self.region = region
		self.game_type = game_type
		self.session_start = session_start
		self.session_end = session_end
		self.session_status = get_session_status(session_id)

	# def get_session_status(self, session_id):

	def __repr__(self):
		'<MP Game Info %r>' % (self.session_id)

# COMMENTS
class GameMpTeams(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	session_id = db.Column(db.String(25))
	teamname = db.Column(db.String(25))
	color = db.Column(db.String(25))
	
	def __init__(self, session_id, teamname, color):
		# self.id = => serial!
		self.session_id = session_id
		self.teamname = teamname
		self.color = color

	def __repr__(self):
		'<MP Game Teams %r>' % (self.id)

# COMMENTS
class GameMpTeamsPlayers(db.Model):
	team_id = db.Column(db.Integer, primary_key=True, unique=False)
	player_id = db.Column(db.String(25))
	completed_game = db.Column(db.String(25))
	
	def __init__(self, team_id, player_id):
		self.team_id = team_id
		self.player_id = player_id
		# get completed game

	def __repr__(self):
		'<MP Game Team Players %r>' % (self.team_id)

# COMMENTS
class SettingsBadges(db.Model):
	badge_id = db.Column(db.String(25), primary_key=True, unique=True)
	score = db.Column(db.String(25))
	name = db.Column(db.String(25), unique=True)
	image = db.Column(db.String(25), unique=True)
	
	def __init__(self, badge_id, score, name, image):
		self.badge_id = badge_id
		self.score = score
		self.name = name
		self.image = image

	def __repr__(self):
		'<Badges %r>' % (self.badge_id)

# COMMENTS
class SettingsScoresFfa(db.Model):
	score_id = db.Column(db.String(25), primary_key=True, unique=True)
	name = db.Column(db.String(25), unique=True)
	score = db.Column(db.Integer)
	
	def __init__(self, score_id, name, score):
		self.score_id = score_id
		self.name = name
		self.score = score

	def __repr__(self):
		'<Scorelist_FFA %r>' % (self.score_id)

# COMMENTS
class SettingsRegions(db.Model):
	region_short = db.Column(db.String(25), primary_key=True, unique=True)
	regionname = db.Column(db.String(120), unique=True)
	country = db.Column(db.Integer)

	def __init__(self, regionname, region_short, country):
		self.region_short = region_short
		self.regionname = regionname
		self.country = country

	def __repr__(self):
		'<Regions %r>' % (self.region_short)

# COMMENTS
class ScheduleSpMotw(db.Model):
	week_id = db.Column(db.String(35), primary_key=True, unique=True)
	ammenity = db.Column(db.String(25))
	time_start = db.Column(db.Date())
	time_end = db.Column(db.Date())
	area = db.Column(db.String(25))
	
	def __init__(self, ammenity, time_start, time_end, area):
		#self. week_id  => serial!
		self.ammenity = ammenity
		self.time_start = time_start
		self.time_end = time_end
		self.area = area

	def __repr__(self):
		'<Schedule MOTW %r>' % (self.week_id)

# COMMENTS
class SettingsAmmenities(db.Model):
	ammenity = db.Column(db.String(35), primary_key=True, unique=True)
	long_name = db.Column(db.String(50), unique=True)
	
	def __init__(self, ammenity, long_name):
		self.ammenity = ammenity
		self.long_name = long_name

	def __repr__(self):
		'<Ammenities %r>' % (self.ammenity)

