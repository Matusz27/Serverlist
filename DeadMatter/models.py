from DeadMatter import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from datetime import datetime



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    email_conf = db.Column(db.Boolean, nullable=False, default=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    servers_id = db.relationship('Servers', backref='author', lazy=True)
    rank_id = db.Column(db.Integer, db.ForeignKey(
        'ranks.id'), nullable=False, default=1)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Ranks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank_name = db.Column(db.String(30), nullable=False, unique=True)
    users = db.relationship('User', backref='Rank', lazy=True)

    def __repr__(self):
        return f"Rank('{self.rank_name}')"
    
    
class Servers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False, unique=True)
    server_IP = db.Column(db.String(15), nullable=False, unique=True)
    port = db.Column(db.Integer)
    description = db.Column(db.String(200), nullable=False)
    discord = db.Column(db.String(100))
    website = db.Column(db.String(100))
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    votes = db.Column(db.Integer(), nullable=False, default=1)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey(
        'country.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.name}', '{self.server_IP}', '{self.image_file}')"
    

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(30), nullable=False, unique=True)
    image_file = db.Column(db.String(20), nullable=False)
    servers = db.relationship('Servers', backref='country', lazy=True)
    
    def __repr__(self):
        return f"Country('{self.country_name}', '{self.image_file}')"

