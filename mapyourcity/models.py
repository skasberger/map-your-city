from mapyourcity import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# COMMENTS
class Player(db.Model):
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
	latlng = db.Column(db.String(36), unique=False) #aktuelle koordinaten
	game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
	game = db.relationship('Game', backref=db.backref('players', lazy='dynamic'))
	score_id = db.Column(db.Integer, db.ForeignKey('scores.id'))
	score = db.relationship('Scores', backref=db.backref('players', lazy='dynamic'))
	theme = db.Column(db.String(15))
	
	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.pw_hash = self.get_hash(password)
		self.created_at = datetime.now()
		self.last_login = datetime.now()
		self.score = Scores(self.username,self.id)

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
		self.country = Regions.query.filter_by(regionname = region).first()
	
	def connect_osm(self, login, password):
		self.osm_login = login
		self.osm_hash = hash_password(password)

	def set_language(self, lang_short):
		self.lang_short = lang_short
	
	def set_username(self, username):
		self.username = username

	def set_email(self, email):
		self.email = email

	def set_last_login(self):
		self.last_login = datetime.now()

	def __repr__(self):
		'<Player %r>' % (self.username)

# COMMENTS
class Scores(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(25), unique=True)
	user_id = db.Column(db.Integer, unique=True)
	score_all = db.Column(db.Integer)
	score_game = db.Column(db.Integer)
	score_week = db.Column(db.Integer)
	created_at = db.Column(db.Date())
	updated_at = db.Column(db.Date())

	def __init__(self, username, user_id): #Wird nur einemal ausgefuehrt, wenn Spieler registriert wird
		self.username = username
		self.user_id = user_id
		self.score_all = 0
		self.score_game = 0
		self.score_week = 0
		self.created_at = datetime.now()
		self.updated_at = datetime.now()

	def init_score_game(self): #Zum reseten des currentGame Scores
		self.score_game = 0

	def init_score_week(self): #Zum resetten der temporaeren Scores
		self.score_week = 0

	def update(self, score):
		self.score_all += score
		self.score_game  += score
		self.score_week += score
		self.updated_at = datetime.now()

	def __repr__(self):
		'<Score %r>' % (self.username)

# COMMENTS
class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	player_id = db.Column(db.Integer)
	region = db.Column(db.String(25))
	game_type = db.Column(db.String(25)) #Singleplayer/Multiplayer
	game_mode = db.Column(db.String(25)) #FFA/MapperOfTheWeek/...
	session_start = db.Column(db.Date())
	session_end = db.Column(db.Date())
	session_status = db.Column(db.String(20))

	def __init__(self, player_id, region, game_type, game_mode):
		self.player_id = player_id
		self.region = region
		self.game_type = game_type
		self.session_start = datetime.now()
		self.session_status = 'started'
	
	def __repr__(self):
		'<Game %r>' % (self.player_id)

# COMMENTS
class GameMpFfa(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	duration = db.Column(db.Integer)
	pw_hash = db.Column(db.String(160))
	max_player = db.Column(db.Integer)
	num_teams = db.Column(db.Integer)
	wheelchair = db.Column(db.Boolean)
	smoking = db.Column(db.Boolean)
	vegetarian = db.Column(db.Boolean)

	def __init__(self, duration, password, max_player, num_teams):
		self.duration = duration
		self.pw_hash = self.get_hash(password)
		self.max_player = max_player
		self.num_teams = num_teams
	
	def get_hash(self, password):
		return generate_password_hash(password)

	#def set_geoobjects(self, ):
		

	def __repr__(self):
		'<SP Game Info %r>' % (self.session_id)

# COMMENTS
class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	game_id = db.Column(db.Integer)
	name = db.Column(db.String(50))
	color = db.Column(db.String(7))
	
	def __init__(self, game_id, name, color):
		self.game_id = game_id
		self.name = name
		self.color = color

	def __repr__(self):
		'<Team %r>' % (self.name)

# COMMENTS
class TeamPlayer(db.Model):
	team_id = db.Column(db.Integer, primary_key=True)
	player_id = db.Column(db.Integer)
	
	def __init__(self, team_id, player_id):
		self.team_id = team_id
		self.player_id = player_id

	def __repr__(self):
		'<Team Player %r>' % (self.player_id)

# COMMENTS
class History(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
	player_id = db.Column(db.Integer)
	score = db.Column(db.Integer)
	event_type = db.Column(db.String(15)) # badge, osm, social
	timestamp = db.Column(db.Date())
	
	def __init__(self, game_id, player_id, event_type):
		self.score = 1 # set dynamically
		self.game_id = game_id
		self.player_id = player_id
		self.event_type = event_type
		self.timestamp = datetime.now()

	#def __repr__(self):
	#	'<History Scores %r %r>' % (self.game_id, self.player_id) 

# COMMENTS
class HistoryGeo(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True) # relate with Scores.id
	object_id = db.Column(db.String(25))
	object_name = db.Column(db.String(150))
	object_type = db.Column(db.String(50))
	object_attributes = db.Column(db.String(150))
	object_latlng = db.Column(db.String(36), unique=False)
	
	def __init__(self, history_id, object_id, object_name, object_type, object_attribute, object_latlng):
		self.id = history_id
		self.object_id = object_id
		self.object_name = object_name
		self.object_type = object_type
		self.object_attributes = object_attribute
		self.object_latlng = object_latlng

	def __repr__(self):
		'<History Geoobjects %r>' % (self.object_id)

# COMMENTS
class HistoryBadges(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	badge_id = db.Column(db.Integer)

	def __init__(self, badge_id):
		self.badge_id = badge_id 

	def __repr__(self):
		'<History Badges %r>' % (self.badge_id)

# COMMENTS
class HistorySocial(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	social_type = db.Column(db.String(50))
	description = db.Column(db.String(500))

	def __init__(self, social_type):
		self.social_type = social_type
		
	def __repr__(self):
		'<History Social %r>' % (self.social_type)

# COMMENTS
class SettingsGameModes(db.Model):
	name_short = db.Column(db.String(25), primary_key=True, unique=True)
	name_long = db.Column(db.String(25), primary_key=True, unique=True)
	game_type = db.Column(db.String(25))
	
	def __init__(self, name_short, name_long, game_type):
		self.name_short = name_short
		self.name_long = name_long
		self.game_type = game_type
		
	def __repr__(self):
		'<Settings Gamemodes %r>' % (self.name_short)

# COMMENTS
class Regions(db.Model):
	region_short = db.Column(db.String(25), primary_key=True, unique=True)
	region_full = db.Column(db.String(120), unique=True)
	country_short = db.Column(db.String(5))
	country_full = db.Column(db.String(100))

	def __init__(self, region_short, region_full, country_short, country_full):
		self.region_short = region_short
		self.region_full = region_full
		self.country_short = country_short
		self.country_full = country_full

	def __repr__(self):
		'<Regions %r>' % (self.region_short)

# COMMENTS
class Badges(db.Model):
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
class OsmObjects(db.Model):
	title = db.Column(db.String(35), primary_key=True, unique=True)
	full_name = db.Column(db.String(50))
	description = db.Column(db.String(300))
	webpage = db.Column(db.String(100))
	wheelchair = db.Column(db.Boolean)
	opening_hours = db.Column(db.Boolean)
	smoking = db.Column(db.Boolean)
	vegan = db.Column(db.Boolean)
	vegetarian = db.Column(db.Boolean)
	kitchen = db.Column(db.Boolean)
	shelter = db.Column(db.Boolean)
	bench = db.Column(db.Boolean)
	bin = db.Column(db.Boolean)

	def __init__(self, title, full_name):
		self.title = title
		self.full_name = full_name

	def __repr__(self):
		'<OSM Objects %r>' % (self.title)

# COMMENTS
class ScheduleSpMotw(db.Model):
	week_id = db.Column(db.Integer, primary_key=True, unique=True)
	object_type = db.Column(db.String(25)) # save as string for better reproducability
	time_start = db.Column(db.Date())
	time_end = db.Column(db.Date())
	area = db.Column(db.String(25)) # store as string => world/<country>/<region>
	
	def __init__(self, object_type, time_start, time_end, area):
		self.object_type = object_type
		self.time_start = time_start
		self.time_end = time_end
		self.area = area

	def __repr__(self):
		'<Schedule MOTW %r>' % (self.time_start)

