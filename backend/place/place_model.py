from app import db, ma

# Place Class/Model
class Place(db.Model):
  __tablename__ = 'place'
  id = db.Column(db.Integer, primary_key=True)
  public_id = db.Column(db.String(50), unique = True)
  user_id = db.Column(db.String(50))
  firstname = db.Column(db.String(50))
  lastname = db.Column(db.String(50))
  place = db.Column(db.String(50))
  date = db.Column(db.String(50))
  team = db.Column(db.String(50))
  floor = db.Column(db.String(50))
  
  def __init__(self, dictionary):
    for k, v in dictionary.items():
        setattr(self, k, v)
# Place schema
class PlaceSchema(ma.Schema):
  class Meta:
    fields = ('public_id', 'user_id', 'firstname', 'lastname', 'place', 'date', 'team', 'floor')

# Init place schemas
place_schema = PlaceSchema()
places_schema = PlaceSchema(many=True)