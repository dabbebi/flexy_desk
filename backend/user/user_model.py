from app import db, ma

# User Class/Model
class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  public_id = db.Column(db.String(50), unique = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  username = db.Column(db.String(100))
  email = db.Column(db.String(100))
  password = db.Column(db.String(400))
  privilege = db.Column(db.String(100))
  
  def __init__(self, dictionary):
    for k, v in dictionary.items():
        setattr(self, k, v)
# User schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('public_id', 'firstname', 'lastname', 'email', 'privilege', 'username')

# Init user schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)