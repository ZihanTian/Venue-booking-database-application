#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
from flask_migrate import Migrate 
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime
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
#artist_genre = db.Table('artist_genre',
#    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
#    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
#)

#venue_genre = db.Table('venue_genre',
#    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
#    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
#)
'''todo = Venue(name = 'Zihan',city = 'Ann Arbor',state='Michigan',address='2445 Lancashire Dr.',phone='7345464295',image_link='none',facebook_link='None',genres='Jazz')
    db.session.add(todo)
    db.session.commit()'''
class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    shows = db.relationship('Show',backref='place',lazy=True)
    seeking_talent = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String(500),nullable=True)
    #genres = db.relationship('Genre', secondary=venue_genre,
    #  backref=db.backref('venues', lazy=True))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean,default=False)
    
    seeking_description = db.Column(db.String(500),nullable=True)
    shows = db.relationship('Show',backref='owner',lazy=True)
    #genres = db.relationship('Genre', secondary=artist_genre,
    #  backref=db.backref('artist', lazy=True))
    #past_shows = db.relationship('Show',backref='artist',lazy=True)
    #upcoming_shows = db.relationship('Show', backref='artist', lazy=True)



    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer,db.ForeignKey('artists.id'), nullable=False)
  venue_id = db.Column(db.Integer,db.ForeignKey('venues.id'), nullable=False)
  start_time = db.Column(db.DateTime,nullable=False)

#class Genre(db.Model):
#  __tablename__ = 'Genre'
#  id = db.Column(db.Integer, primary_key=True)
#  genre = db.Column(db.String(120),nullable=False)



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
#todo = Venue(name = 'Zihan',city = 'Ann Arbor',state='Michigan',address='2445 Lancashire Dr.',phone='7345464295',image_link='none',facebook_link='None',genres='Jazz')
#db.session.add(todo)
#db.session.commit()
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
  all_venues = Venue.query.all()
  data = []
  city_map = {}
  for venue in all_venues:
    unique_key = venue.city + ' ' + venue.state 
    if unique_key in city_map:
      venue_record = {}
      venue_record['id'] = venue.id 
      venue_record['name'] = venue.name
      comings = len(Show.query.join(Venue).filter(Show.venue_id==venue.id,Show.start_time>datetime.now()).all())
      #Show.query.filter()
      #all_shows = venue.shows
      venue_record['num_upcoming_shows'] = comings
      city_map[unique_key]['venues'].append(venue_record) 
    else:
      city_map[unique_key] = {}
      city_map[unique_key]['venues'] = []
      venue_record = {}
      venue_record['id'] = venue.id 
      venue_record['name'] = venue.name
      comings = len(Show.query.join(Venue).filter(Show.venue_id==venue.id,Show.start_time>datetime.now()).all())
      #all_shows = venue.shows
      venue_record['num_upcoming_shows'] = comings
      city_map[unique_key]['venues'].append(venue_record) 
  for unique_key in city_map.keys():
    small_map = {}
    small_map['city'] = unique_key.split(' ')[0]
    small_map['state'] = unique_key.split(' ')[1]
    small_map['venues'] = city_map[unique_key]['venues']
    data.append(small_map)
    
  '''   
  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]'''
  print(data)
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response = {}
  try:
    search_term = request.form.get('search_term','')
    #print(search_term)
    #print('hererererere')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    response['count'] = len(venues)
    response['data'] = []
    for venue in venues:
      small_map = {}
      small_map['id'] = venue.id 
      small_map['name'] = venue.name 
      shows = Show.query.join(Venue).filter(Show.venue_id==venue.id, Show.start_time>datetime.now()).all()
      print(shows)
      small_map['num_upcoming_shows'] = len(shows)
      response['data'].append(small_map)
  except:
    error = True
    print(sys.exc_info())
  '''response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }'''
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
#-----------------------------------------------------------------------------------------------------------------------
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  data = {}
  data['id'] = venue.id 
  data['name'] = venue.name 
  data['genres'] = venue.genres 
  data['address'] = venue.address 
  data['city'] = venue.city 
  data['state'] = venue.state 
  data['phone'] = venue.phone 
  if venue.website:
    data['website'] = venue.website 
  else:
    data['website'] = ''
  data['facebook_link'] = venue.facebook_link 
  if venue.seeking_talent:
    data['seeking_talent'] = True 
    data['seeking_description'] = venue.seeking_description
  else:
    data['seeking_talent'] = False 
  data['image_link'] = venue.image_link
  data['past_shows'] = []
  
  past_shows = Show.query.join(Venue).filter(Show.venue_id==venue.id, Show.start_time <= datetime.now()).all()
  data['past_shows_count'] = len(past_shows)
  for show in past_shows:
    past_map = {}
    past_map['artist_id'] = show.artist_id
    past_map['artist_name'] = Artist.query.get(show.artist_id).name 
    past_map['artist_image_link'] = Artist.query.get(show.artist_id).image_link 
    past_map['start_time'] = (show.start_time).strftime("%m/%d/%YT%H:%M:%S") 
    data['past_shows'].append(past_map)
  
  data['upcoming_shows'] = []
  upcoming_shows = Show.query.join(Venue).filter(Show.venue_id==venue.id, Show.start_time > datetime.now()).all()
  data['upcoming_shows_count'] = len(upcoming_shows)
  for show in upcoming_shows:
    coming_shows = {}
    coming_shows['artist_id'] = show.artist_id
    coming_shows['artist_name'] = Artist.query.get(show.artist_id).name 
    coming_shows['artist_image_link'] = Artist.query.get(show.artist_id).image_link 
    coming_shows['start_time'] = (show.start_time).strftime("%m/%d/%YT%H:%M:%S") 
    data['upcoming_shows'].append(coming_shows)
  '''data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]'''
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
  try:
    print(request.form)
    name = request.form.get('name','')
    city = request.form.get('city','')
    state = request.form.get('state','')
    address = request.form.get('address','')
    phone = request.form.get('phone','')
    
    image_link = request.form.get('image_link','')
    facebook_link = request.form.get('facebook_link','')
    genres = request.form.getlist('genres')
    genres = ' '.join(genres)
    venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link,genres=genres)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + venue.name + ' was successfully listed!')
  except:
    flash('An error occurred. Venue ' + request.form.get('name','') + ' could not be listed.')
  finally:
    db.session.close()
  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #name = request.form.get('name','')

  #print(contact)
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id==venue_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
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
  all_artists = Artist.query.all()
  data = []
  for artist in all_artists:
    small_map = {}
    small_map['id'] = artist.id
    small_map['name'] = artist.name
    data.append(small_map)
  '''data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]'''
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response = {}
  try:
    search_term = request.form.get('search_term','')
    #print(search_term)
    #print('hererererere')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    response['count'] = len(artists)
    response['data'] = []
    for artist in artists:
      small_map = {}
      small_map['id'] = artist.id 
      small_map['name'] = artist.name 
      shows = Show.query.join(Artist).filter(Show.artist_id==artist.id, Show.start_time>datetime.now()).all()
      #print(shows)
      small_map['num_upcoming_shows'] = len(shows)
      response['data'].append(small_map)
    #print(response['data'])
  except:
    error = True
    print(sys.exc_info())
  '''response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }'''
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)
  data = {}
  data['id'] = artist.id 
  data['name'] = artist.name 
  data['genres'] = artist.genres.split(' ') 
  #data['address'] = venue.address 
  data['city'] = artist.city 
  data['state'] = artist.state 
  data['phone'] = artist.phone 
  if artist.website:
    data['website'] = artist.website 
  #else:
  #  data['website'] = ''
  data['facebook_link'] = artist.facebook_link 
  if artist.seeking_venue:
    data['seeking_venue'] = True 
    data['seeking_description'] = artist.seeking_description
  else:
    data['seeking_venue'] = False 
  data['image_link'] = artist.image_link
  data['past_shows'] = []
  
  past_shows = Show.query.join(Artist).filter(Show.artist_id==artist.id, Show.start_time <= datetime.now()).all()
  data['past_shows_count'] = len(past_shows)
  for show in past_shows:
    past_map = {}
    past_map['venue_id'] = show.venue_id
    past_map['venue_name'] = Venue.query.get(show.venue_id).name 
    past_map['venue_image_link'] = Venue.query.get(show.venue_id).image_link 
    past_map['start_time'] = (show.start_time).strftime("%m/%d/%YT%H:%M:%S") 
    data['past_shows'].append(past_map)
  
  data['upcoming_shows'] = []
  upcoming_shows = Show.query.join(Artist).filter(Show.artist_id==artist.id, Show.start_time > datetime.now()).all()
  data['upcoming_shows_count'] = len(upcoming_shows)
  for show in upcoming_shows:
    coming_shows = {}
    coming_shows['venue_id'] = show.venue_id
    coming_shows['venue_name'] = Venue.query.get(show.venue_id).name 
    coming_shows['venue_image_link'] = Venue.query.get(show.venue_id).image_link 
    coming_shows['start_time'] = (show.start_time).strftime("%m/%d/%YT%H:%M:%S")
    data['upcoming_shows'].append(coming_shows)
  #print(data,'herererere')
  return render_template('pages/show_artist.html', artist=data)
  #return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  try:
    artist = {}
    artist['id'] = artist_id
    art = Artist.query.get(artist_id)
    artist['name'] =  art.name 
    artist['genres'] = art.genres.split(' ')
    artist['city'] = art.city
    artist['state'] = art.state
    artist['phone'] = art.phone
    artist['website'] = art.website
    artist['facebook_link'] = art.facebook_link
    artist['seeking_venue'] = art.seeking_venue
    artist['seeking_description'] = art.seeking_description
    artist['image_link'] = art.image_link
  except:
    error = True
    print(sys.exc_info())

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    artist_class = Artist.query.get(artist_id)
    artist_class.name = request.form.get('name')
    artist_class.genres =request.form.get('genres') 
    artist_class.city = request.form.get('city')
    artist_class.state = request.form.get('state')
    artist_class.phone = request.form.get('phone')
    artist_class.website = request.form.get('website')
    artist_class.facebook_link = request.form.get('facebook_link')
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = {}
  ven = Venue.query.get(venue_id)
  venue['name'] = ven.name
  venue['genres'] = ven.genres.split(' ')
  venue['address'] = ven.address
  venue['city'] = ven.city
  venue['state'] = ven.state
  venue['phone'] = ven.phone
  venue['website'] = ven.website
  venue['facebook_link'] = ven.facebook_link
  venue['seeking_talent'] = ven.seeking_talent
  venue['seeking_description'] = ven.seeking_description
  venue['image_link'] = ven.image_link
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    venue = Venue.query.get(venue_id)
    venue.name = request.form.get('name')
    venue.name = request.form.get('name','')
    venue.city = request.form.get('city','')
    venue.state = request.form.get('state','')
    venue.address = request.form.get('address','')
    venue.phone = request.form.get('phone','')
    
    venue.image_link = request.form.get('image_link','')
    venue.facebook_link = request.form.get('facebook_link','')
    genres = request.form.getlist('genres')
    venue.genres = ' '.join(genres)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
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
  try:
    print(request.form)
    name = request.form.get('name','')
    city = request.form.get('city','')
    state = request.form.get('state','')
    #address = request.form.get('address','')
    phone = request.form.get('phone','')
    
    image_link = request.form.get('image_link','')
    facebook_link = request.form.get('facebook_link','')
    genres = request.form.getlist('genres')
    genres = ' '.join(genres)
    artist = Artist(name=name,city=city,state=state,phone=phone,image_link=image_link,facebook_link=facebook_link,genres=genres)
    db.session.add(artist)
    db.session.commit()
    flash('Venue ' + artist.name + ' was successfully listed!')
  except:
    flash('An error occurred. Venue ' + request.form.get('name','') + ' could not be listed.')
  finally:
    db.session.close()
  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
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
  all_shows = Show.query.all()
  data = []
  for show in all_shows:
    small_map = {}
    small_map['venue_id'] = show.venue_id
    small_map['venue_name'] = Venue.query.get(show.venue_id).name
    small_map['artist_id'] = show.artist_id
    small_map['artist_image_link'] = Artist.query.get(show.artist_id).image_link
    small_map['start_time'] = show.start_time.strftime("%m/%d/%YT%H:%M:%S") 
    data.append(small_map)
  
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
  try:
    print(request.form)
    artist_id = int(request.form.get('artist_id'))
    venue_id = int(request.form.get('venue_id'))
    start_time = request.form.get('start_time')
    if Artist.query.get(artist_id) and Venue.query.get(venue_id):
      show = Show(artist_id=artist_id,venue_id=venue_id,start_time=start_time)
      db.session.add(show)
      db.session.commit()
      print(show.venue_id)
      flash(f'Show at venue {show.venue_id} was successfully listed!')
    else:
      error = True
      flash('An error occurred. the show at venue' + request.form.get(venue_id) +'could not be listed.')
    
  except:

    #error = True
    flash('An error occurred. the show at venue could not be listed.')
  finally:
    db.session.close()
  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  
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
