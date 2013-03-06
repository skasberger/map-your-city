from mapyourcity import app, db
from mapyourcity.models import Player, OsmObjects, Regions
db.drop_all()
db.create_all()
player = Player(username='cheeseman', email='test@test.at', password='test')
player.set_home_region('graz')
db.session.add(player)
db.session.add(Regions(region_short='graz', region_full='Stadt Graz', country_short='at', country_full='Austria'))
db.session.add(OsmObjects(title='amenity=restaurant', full_name='Restaurant'))
db.session.add(OsmObjects(title='amenity=bar', full_name='Bar'))
db.session.add(OsmObjects(title='amenity=bank', full_name='Bank'))
db.session.commit()
exit()
