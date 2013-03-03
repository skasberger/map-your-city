from mapyourcity import app, db
from mapyourcity.models import SettingsPlayer, HistoryGeo
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
  else:
    return render_template('game.html')

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
@app.route('/verify')
def verify():
  if not g.player:
    return redirect(url_for('login'))
  osmid=  request.args.get('ObjectOSMID', 0, type=int)
  name = request.args.get('ObjectName', '', type=str)
  attribute = request.args.get('ObjectAttribute', '', type=str)
  geoObject = HistoryGeo(osmid, name, attribute, g.player.id)
  db.session.add(geoObject)
  g.player.points=g.player.points+1
  db.session.commit()
  return jsonify(result=g.player.points)

# COMMENTS
@app.route('/player')

# COMMENTS
@app.route('/player/<playerid>')

# COMMENTS
@app.route('/player/<playerid>/settings')

# COMMENTS
@app.route('/player/<playerid>/settings/osm')

# COMMENTS
@app.route('/player/<playerid>/map-of-fame')

# COMMENTS
@app.route('/player/<playerid>/score')

# COMMENTS
@app.route('/player/<playerid>/stats')

# COMMENTS
@app.route('/<playerid>/settings')
def player_settings():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

# COMMENTS
@app.route('/sp')

# COMMENTS
@app.route('/sp/ffa')

# COMMENTS
@app.route('/sp/ffa/help')

# COMMENTS
@app.route('/sp/motw')

# COMMENTS
@app.route('/mp')

# COMMENTS
@app.route('/score')
def score():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

# COMMENTS
@app.route('/score/<playerid>')
def scorePlayer():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

# COMMENTS
@app.route('/score/<region>')
def scoreRegion():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

# COMMENTS
@app.route('/score/<country>')
def scoreCountry():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

# COMMENTS
@app.route('/score/world')
def scoreWorld():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

# COMMENTS
@app.route('/about')
def about():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

# COMMENTS
@app.route('/about/terms-of-use')
def aboutTou():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

# COMMENTS
@app.route('/about/code')
def aboutCode():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

# COMMENTS
@app.route('/about/gamemodi')
def aboutGamemodi():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

# COMMENTS
@app.route('/about/gamemodi/sp_motw')
def aboutGamemodiSpMotw():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

# COMMENTS
@app.route('/about/gamemodi/sp_ffa')
def aboutGamemodiSpFfa():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

# COMMENTS
@app.route('/about/data-protection')
def aboutDataProtection():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

