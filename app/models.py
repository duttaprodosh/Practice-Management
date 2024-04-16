from app import db, app
from flask_login import UserMixin
from flask_login import LoginManager
#from app import login
login = LoginManager(app)

@login.user_loader
def load_user(id):
    return User.query.get_id(int(id))

########   USER MODEL ########
class User(db.Model, UserMixin):
#     __tablename__ = 'user'
     id = db.Column(db.Integer, primary_key=True)
     user_name = db.Column(db.String(64), index=True, unique=True )
     password = db.Column(db.String(128))
     def get_id(self):
         return(self.id)

########   Team MODEL ########
class Team(db.Model):
#     __tablename__ = 'team'
     team_id = db.Column(db.Integer, primary_key=True)
     team_name = db.Column(db.String(164), index=True, unique=True )
     team_mascot = db.Column(db.String)
     practices = db.relationship('Practice', backref='practices', lazy=True)
########   Practice MODEL ########
class Practice(db.Model):
#    __tablename__ = 'practice'
    practice_id = db.Column(db.Integer, primary_key=True)

    practice_length = db.Column(db.String(164))
    practice_date = db.Column(db.Date)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
