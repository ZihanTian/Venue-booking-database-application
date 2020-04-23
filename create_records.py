venue1 = Venue(name='The musical hop',city='San Francisco',state='CA',address='1015 Folsom Street',phone='123-123-1234',image_link='',facebook_link='https://www.facebook.com/TheMusicalHop',genres='Jazz')
venue2 = Venue(name='Park square live music & coffee',city='San Francisco',state='CA',address='34 Whiskey Moore Ave',phone='123-321-1234',image_link='',facebook_link='https://www.facebook.com/Thesecondone',genres='Folk')
venue3 = Venue(name='Piano Bar',city='New York',state='NY',address='335 Delancey Street',phone='123-546-1234',image_link='',facebook_link='https://www.facebook.com/PianoBar',genres='Classical')
db.session.add(venue1)
db.session.add(venue2)
db.session.add(venue3)
db.session.commit()
artist1 = Artist(name='Zihan',city='Santa Clara',state='CA',phone='734-546-4295',genres='Classical')
artist2 = Artist(name='Lida',city='Ann Arbor',state='MI',phone='123-555-6667',genres='Folk')
artist3 = Artist(name='Tina',city='New York',state='NY',phone='344-456-7890',genres='Jazz')
show1 = Show(artist_id=1,venue_id=5,start_time=datetime.now())
show2 = Show(artist_id=2,venue_id=4,start_time=datetime.now())
show3 = Show(artist_id=3,venue_id=3,start_time=datetime.now())
db.session.add(artist1)
db.session.add(artist2)
db.session.add(artist3)
db.session.add(show1)
db.session.add(show2)
db.session.add(show3)
db.session.commit()
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
    small_map['venues'] = city_map[unique_key]
    data.append(small_map)
