from mapyourcity import app, db
from mapyourcity.models import Player, POI
from flask import Flask, request, session, g, jsonify, redirect, url_for, \
	abort, render_template, flash

@app.before_request
def before_request():
  g.player = None
  if 'player_id' in session:
    g.player = Player.query.filter_by(id = session['player_id']).first()

@app.route('/')
def game():
  if not g.player:
    return redirect(url_for('login'))
  else:
    return render_template('game.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    player = Player.query.filter_by(username = request.form['username']).first()
    if player is not None and player.check_password(request.form['password']):
      session['player_id'] = player.id
      return redirect(url_for('game'))
    else:
      error = 'Wrong Username or Password'
  else:
    flash('Already logged in')
  return render_template('login.html', error = error)

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
    elif Player.query.filter_by(username = request.form['username']).first() is not None:
      error = 'The username is already taken'
    else:
      g.player=None
      player = Player(request.form['username'], request.form['email'], request.form['password'])
      db.session.add(player)
      db.session.commit()
      flash('Successfully registered!')
      return redirect(url_for('login'))
  return render_template('register.html', error=error)

@app.route('/logout')
def logout():
  session.pop('player_id', None)
  g.player = None
  return redirect(url_for('login'))

@app.route('/verify')
def verify():
  if not g.player:
    return redirect(url_for('login'))
  osmid=  request.args.get('ObjectOSMID', 0, type=int)
  name = request.args.get('ObjectName', '', type=str)
  attribute = request.args.get('ObjectAttribute', '', type=str)
  poi = POI(osmid, name, attribute, g.player.id)
  db.session.add(poi)
  g.player.points=g.player.points+1
  db.session.commit()
  return jsonify(result=g.player.points)

@app.route('/player')
def remove_player(playerid):
  if not g.player:
  abort(401)
  
  player = Player.query.filter_by(id = playerid).first()

  db.session.delete(player);
  db.session.commit();
  flash('Player with Title:' + player.name + ' was removed')
  return redirect(url_for('game'))

@app.route('/player/<playerid>')
def remove_player(playerid):
  if not g.player:
  abort(401)
  
  player = Player.query.filter_by(id = playerid).first()

  db.session.delete(player);
  db.session.commit();
  flash('Player with Title:' + player.name + ' was removed')
  return redirect(url_for('game'))

@app.route('/player/<playerid>/settings')
def remove_player(playerid):
  if not g.player:
  abort(401)
  
  player = Player.query.filter_by(id = playerid).first()

  db.session.delete(player);
  db.session.commit();
  flash('Player with Title:' + player.name + ' was removed')
  return redirect(url_for('game'))

@app.route('/player/<playerid>/settings/osm')
def remove_player(playerid):
  if not g.player:
  abort(401)
  
  player = Player.query.filter_by(id = playerid).first()

  db.session.delete(player);
  db.session.commit();
  flash('Player with Title:' + player.name + ' was removed')
  return redirect(url_for('game'))

@app.route('/player/<playerid>/map-of-fame')
def remove_player(playerid):
  if not g.player:
  abort(401)
  
  player = Player.query.filter_by(id = playerid).first()

  db.session.delete(player);
  db.session.commit();
  flash('Player with Title:' + player.name + ' was removed')
  return redirect(url_for('game'))

@app.route('/player/<playerid>/score')
def remove_player(playerid):
  if not g.player:
  abort(401)
  
  player = Player.query.filter_by(id = playerid).first()

  db.session.delete(player);
  db.session.commit();
  flash('Player with Title:' + player.name + ' was removed')
  return redirect(url_for('game'))

@app.route('/player/<playerid>/stats')
def remove_player(playerid):
  if not g.player:
  abort(401)
  
  player = Player.query.filter_by(id = playerid).first()

  db.session.delete(player);
  db.session.commit();
  flash('Player with Title:' + player.name + ' was removed')
  return redirect(url_for('game'))

@app.route('/sp')
def remove_player(playerid):
  if not g.player:
  abort(401)
  
  player = Player.query.filter_by(id = playerid).first()

  db.session.delete(player);
  db.session.commit();
  flash('Player with Title:' + player.name + ' was removed')
  return redirect(url_for('game'))

@app.route('/sp/ffa')
def remove_player(playerid):
  if not g.player:
  abort(401)
  
  player = Player.query.filter_by(id = playerid).first()

  db.session.delete(player);
  db.session.commit();
  flash('Player with Title:' + player.name + ' was removed')
  return redirect(url_for('game'))

@app.route('/sp/ffa/help')
def remove_player(playerid):
  if not g.player:
  abort(401)
  
  player = Player.query.filter_by(id = playerid).first()

  db.session.delete(player);
  db.session.commit();
  flash('Player with Title:' + player.name + ' was removed')
  return redirect(url_for('game'))

@app.route('/sp/motw')
def remove_player(playerid):
  if not g.player:
  abort(401)
  
  player = Player.query.filter_by(id = playerid).first()

  db.session.delete(player);
  db.session.commit();
  flash('Player with Title:' + player.name + ' was removed')
  return redirect(url_for('game'))

@app.route('/mp')
def remove_player(playerid):
  if not g.player:
  abort(401)
  
  player = Player.query.filter_by(id = playerid).first()

  db.session.delete(player);
  db.session.commit();
  flash('Player with Title:' + player.name + ' was removed')
  return redirect(url_for('game'))

@app.route('/scores')
def show_score():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

@app.route('/scores/<playerid>')
def show_score():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

@app.route('/scores/<region>')
def show_score():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

@app.route('/scores/<country>')
def show_score():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

@app.route('/scores/world')
def show_score():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('scores.html')

@app.route('/about')
def show_info():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

@app.route('/about/terms-of-use')
def show_info():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

@app.route('/about/code')
def show_info():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

@app.route('/about/gamemodi')
def show_info():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

@app.route('/about/gamemodi/sp_motw')
def show_info():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

@app.route('/about/gamemodi/sp_ffa')
def show_info():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

@app.route('/about/data-protection')
def show_info():
  if not g.player:
    return redirect(url_for('login'))
  return render_template('info.html')

