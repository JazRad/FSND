#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app,db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    website = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Shows', backref='shows_venue', lazy=True)
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Shows', backref='shows_artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Shows(db.Model):
  __tablename__ = 'Shows'

  id = db.Column(db.Integer,primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  areas = Venue.query.with_entities(Venue.city, Venue.state).distinct()
  data = []

  for area in areas:
    venues = Venue.query.filter_by(city=area.city, state=area.state).all()
    venue_data = []
    
    for venue in venues:
      num_upcoming_shows = 0
      shows = Shows.query.filter_by(venue_id=venue.id).all()
      now = datetime.now()
        
      for show in shows:
        if show.start_time > now:
          num_upcoming_shows +=1
        
      venue_data.append({
      'id': venue.id,
      'name': venue.name,
      'num_upcoming_shows': num_upcoming_shows,
      })

    data.append({
      'city': area.city,
      'state': area.state,
      'venues':venue_data
    })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  print(search_term)

  results = Venue.query.filter(Venue.name.ilike('%' + search_term + '%'))
  print(results)
  result_count = 0
  response = []
  data = []

  for result in results:
    num_upcoming_shows = 0
    result_count += 1
    shows = Shows.query.filter_by(venue_id=result.id).all()
    now = datetime.now()

    for show in shows:
      if show.start_time > now:
          num_upcoming_shows +=1

    data.append({
      'id': result.id,
      'name': result.name,
      'num_upcoming_shows': num_upcoming_shows
    })

  response = {
    'count': result_count,
    'data': data
    }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  #Get shows information
  last_shows = db.session.query(Artist, Shows).join(Venue).filter(
    Shows.artist_id == Artist.id,
    Shows.venue_id == venue_id,
    Shows.start_time<datetime.now()
  ).all()
  
  next_shows = db.session.query(Artist, Shows).join(Venue).filter(
    Shows.artist_id == Artist.id,
    Shows.venue_id == venue_id,
    Shows.start_time>datetime.now()
  ).all()

  venue = Venue.query.get(venue_id)

  #Get venue information
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": [{
      'artist_id': artist.id,
      'artist_name': artist.name,
      'artist_image_link': artist.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    } for artist, show in last_shows],
    "upcoming_shows": [{
      'artist_id': artist.id,
      'artist_name': artist.name,
      'artist_image_link': artist.image_link,
      'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    } for artist, show in next_shows],
    "past_shows_count": len(last_shows),
    "upcoming_shows_count": len(next_shows),
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error=False
 
  venue = Venue()
  venue.name = request.form['name']
  venue.city = request.form['city']
  venue.state = request.form['state']
  venue.address = request.form['address']
  venue.phone = request.form['phone']
  venue.genres = request.form.getlist('genres')
  venue.facebook_link = request.form['facebook_link']
  venue.image_link = request.form['image_link']
  venue.website = request.form['website']
  venue.seeking_description = request.form['seeking_description']
  
  #Convert seeking_talent to boolean
  if (request.form['seeking_talent'] == 'y'):
    venue.seeking_talent = True
  else:
    venue.seeking_talent = False

  try:
    db.session.add(venue)
    db.session.commit()
  
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  
  finally:
    db.session.close()
    if error:
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        flash('An error occured. Venue ' + request.form['name'] + ' could not be listed!')

    else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # on successful db insert, flash success
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  
  except:
    db.session.rollback()

  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()

  return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search_term = request.form.get('search_term')
  print(search_term)

  results = Artist.query.filter(Artist.name.ilike('%' + search_term + '%'))
  print(results)
  result_count = 0
  response = []
  data = []

  for result in results:
    num_upcoming_shows = 0
    result_count += 1
    shows = Shows.query.filter_by(artist_id=result.id).all()
    now = datetime.now()

    for show in shows:
      if show.start_time > now:
          num_upcoming_shows +=1

    data.append({
      'id': result.id,
      'name': result.name,
      'num_upcoming_shows': num_upcoming_shows
    })

  response = {
    'count': result_count,
    'data': data
    }
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  last_shows = db.session.query(Venue, Shows).join(Artist).filter(
    Shows.artist_id == artist_id,
    Shows.venue_id == Venue.id,
    Shows.start_time<datetime.now()
    ).all()
  
  next_shows = db.session.query(Venue, Shows).join(Artist).filter(
    Shows.artist_id == artist_id,
    Shows.venue_id == Venue.id,
    Shows.start_time>datetime.now()
  ).all()
  
  #Get artist information
  artist = Artist.query.get(artist_id)
  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [{
        'venue_id': venue.id,
        'venue_name': venue.name,
        'venue_image_link': venue.image_link,
        'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    } for venue, show in last_shows],
    "upcoming_shows": [{
        'venue_id': venue.id,
        'venue_name': venue.name,
        'venue_image_link': venue.image_link,
        'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    } for venue, show in next_shows],
    "past_shows_count": len(last_shows),
    "upcoming_shows_count": len(next_shows),
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist= Artist.query.get(artist_id)

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error=False
 
  artist = Artist.query.get(artist_id)
  artist.name = request.form['name']
  artist.city = request.form['city']
  artist.state = request.form['state']
  artist.phone = request.form['phone']
  artist.genres = request.form.getlist('genres')
  artist.facebook_link = request.form['facebook_link']
  artist.image_link = request.form['image_link']
  artist.website = request.form['website']
  artist.seeking_description = request.form['seeking_description']
  
  #Convert seeking_talent to boolean
  if (request.form['seeking_venue'] == 'y'):
    artist.seeking_venue = True
  else:
    artist.seeking_venue = False

  try:
    db.session.commit()
  
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  
  finally:
    db.session.close()
    if error:
      flash('An error occured. Artist ' + request.form['name'] + ' could not be updated!')
    else:
      flash('Artist ' + request.form['name'] + ' was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  
  error=False
 
  venue = Venue.query.get(venue_id)
  venue.name = request.form['name']
  venue.city = request.form['city']
  venue.state = request.form['state']
  venue.address = request.form['address']
  venue.phone = request.form['phone']
  venue.genres = request.form.getlist('genres')
  venue.facebook_link = request.form['facebook_link']
  venue.image_link = request.form['image_link']
  venue.website = request.form['website']
  venue.seeking_description = request.form['seeking_description']
  
  #Convert seeking_talent to boolean
  if (request.form['seeking_talent'] == 'y'):
    venue.seeking_talent = True
  else:
    venue.seeking_talent = False

  try:
    db.session.commit()
  
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  
  finally:
    db.session.close()
    if error:
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be updated.')
        flash('An error occured. Venue ' + request.form['name'] + ' could not be updated!')

    else:
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
  # on successful db insert, flash success
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  #TODO: take values from the form submitted, and update existing
  #venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error=False
 
  artist = Artist()
  artist.name = request.form['name']
  artist.city = request.form['city']
  artist.state = request.form['state']
  artist.phone = request.form['phone']
  artist.genres = request.form.getlist('genres')
  artist.facebook_link = request.form['facebook_link']
  artist.image_link = request.form['image_link']
  artist.website = request.form['website']
  artist.seeking_description = request.form['seeking_description']
  
  #Convert seeking_talent to boolean
  if (request.form['seeking_venue'] == 'y'):
    artist.seeking_venue = True
  else:
    artist.seeking_venue = False

  try:
    db.session.add(artist)
    db.session.commit()
  
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  
  finally:
    db.session.close()
    if error:
  # on successful db insert, flash success
      flash('An error occured. Artist ' + request.form['name'] + ' could not be listed!')
    else:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Shows.query.all()
  data = []

  for show in shows:
    venue = Venue.query.get(show.venue_id)
    artist = Artist.query.get(show.artist_id)

    data.append({
      'venue_id': venue.id,
      'venue_name':venue.name,
      'artist_id': artist.id,
      'artist_name':artist.name,
      'artist_image_link':artist.image_link,
      'start_time':show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False

  show = Shows()
  show.venue_id = request.form['venue_id']
  show.artist_id = request.form['artist_id']
  show.start_time =  request.form['start_time']

  try:
    db.session.add(show)
    db.session.commit()
  
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  
  finally:
    db.session.close()
    if error:
      flash('An error occured. Artist ' + request.form['artist_id'] + ' could not be listed!')
    else:
      flash('Show was successfully listed!')
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
