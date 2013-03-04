from mapyourcity import app, db
from mapyourcity.models import SettingsPlayer, HistoryOsm
from flask import Flask, request, session, g, jsonify, redirect, url_for, abort, render_template, flash

# COMMENTS
@app.before_request
def before_request():
  g.player = None
  if 'player_id' in session:
    g.player = SettingsPlayer.query.filter_by(id = str(session['player_id'])).first()

# COMMENTS
@app.route('/')
def main():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('main.html')

# COMMENTS
@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    player = SettingsPlayer.query.filter_by(username = request.form['username']).first()
    if player is not None and player.check_password(request.form['password']):
      session['player_id'] = player.id
      return redirect(url_for('main'))
    else:
      error = 'Wrong Username or Password'
  else:
    flash('Already logged in')
  return render_template('login.html', error = error)

# COMMENTS
@app.route('/register', methods=['POST','GET'])
def register():
  error = None
  if request.method == 'POST':
    if not request.form['username']:
      error = 'You have to enter a username'
    elif not request.form['email'] or \
      '@' not in request.form['email']:
      error = 'You have to enter a valid email address'
    elif not request.form['password']:
      error = 'You have to enter a password'
    elif request.form['password'] != request.form['password2']:
      error = 'The two passwords do not match'
    elif SettingsPlayer.query.filter_by(username = request.form['username']).first() is not None:
      error = 'The username is already taken'
    else:
      g.player=None
      player = SettingsPlayer(request.form['username'], request.form['email'], request.form['password'])
      db.session.add(player)
      db.session.commit()
      flash('Successfully registered!')
      return redirect(url_for('login'))
  return render_template('register.html', error=error)

# COMMENTS
@app.route('/logout')
def logout():
  session.pop('player_id', None)
  g.player = None
  return redirect(url_for('login'))


# COMMENTS
@app.route('/verify-osm')
def verifyOsm():
  if not g.player:
    return redirect(url_for('login'))
  object_id=  request.args.get('ObjectId', 0, type=int)
  name = request.args.get('ObjectName', '', type=str)
  ammenity = request.args.get('ObjectType', '', type=str)
  attribute = request.args.get('ObjectAttr', '', type=str)
  geoObject = HistoryOsm(session, g.player.id, object_id, name, ammenity, attribute)
  db.session.add(geoObject)
  g.player.score=g.player.score+1
  db.session.commit()
  return jsonify(result=g.player.score)

# COMMENTS
@app.route('/player')
def player():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('player.html')

# COMMENTS
# @app.route('/player/<playerid>')

# COMMENTS
# @app.route('/player/<playerid>/settings')

# COMMENTS
# @app.route('/player/<playerid>/settings/osm')

# COMMENTS
# @app.route('/player/<playerid>/map-of-fame')

# COMMENTS
# @app.route('/player/<playerid>/score')

# COMMENTS
# @app.route('/player/<playerid>/stats')

# COMMENTS
#@app.route('/<playerid>/settings')
#def playerSettings():
#  if not g.player:
#    return redirect(url_for('login'))
#  return render_template('game.html')

#@app.route('/player/settings')
#def playerSettings():
#  if not g.player:
#    return redirect(url_for('login'))
#  return render_template('game.html')


# COMMENTS
@app.route('/sp/ffa')
def sp_ffa():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('game_sp_ffa.html')

# COMMENTS
@app.route('/mp/ffa')
def mp_ffa():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('game_mp_ffa.html')

# COMMENTS
@app.route('/scores')
def scores():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

# COMMENTS
# @app.route('/score/<playerid>')
# def scorePlayer():
#   if not g.player:
#     return redirect(url_for('login'))
#  return render_template('score.html')

# COMMENTS
#@app.route('/score/<region>')
#def scoreRegion():
  #if not g.player:
#    return redirect(url_for('login'))
  #return render_template('score.html')

# COMMENTS
#@app.route('/score/<country>')
#def scoreCountry():
#  if not g.player:
#    return redirect(url_for('login'))
#  return render_template('score.html')

# COMMENTS
@app.route('/scores/world')
def scoreWorld():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

# COMMENTS
@app.route('/about')
def about():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('about.html')

# COMMENTS
#@app.route('/about/terms-of-use')
#def aboutTou():
#  if not g.player:
#    return redirect(url_for('login'))
#  return render_template('about.html')

# COMMENTS
#@app.route('/about/code')
#def aboutCode():
#  if not g.player:
#    return redirect(url_for('login'))
#  return render_template('about.html')

# COMMENTS
#@app.route('/about/gamemodi')
#def aboutGamemodi():
#  if not g.player:
#    return redirect(url_for('login'))
#  return render_template('help.html')

# COMMENTS
#@app.route('/about/gamemodi/sp_motw')
#def aboutGamemodiSpMotw():
#  if not g.player:
#    return redirect(url_for('login'))
#  return render_template('help.html')

# COMMENTS
#@app.route('/about/gamemodi/sp_ffa')
#def aboutGamemodiSpFfa():
#  if not g.player:
#    return redirect(url_for('login'))
#  return render_template('help.html')

# COMMENTS
#@app.route('/about/data-protection')
#def aboutDataProtection():
#  if not g.player:
#    return redirect(url_for('login'))
#  return render_template('about.html')

# COMMENTS
@app.route('/help')
def help():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('help.html')

# COMMENTS
@app.route('/help/sp/ffa')
def help_sp_ffa():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('help_sp_ffa.html')

# COMMENTS
@app.route('/help/mp/ffa')
def help_mp_ffa():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('help_mp_ffa.html')

