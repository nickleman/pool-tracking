from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime


class Player(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(255))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    matches_won = db.relationship('Match', backref="winner", foreign_keys='Match.winner_id', lazy=True)
    matches_lost = db.relationship('Match', backref="loser", foreign_keys='Match.loser_id', lazy=True)
    games_won = db.relationship('Game', backref="winner", foreign_keys='Game.winner_id', lazy=True)
    games_lost = db.relationship('Game', backref="loser", foreign_keys='Game.loser_id', lazy=True)

    def __repr__(self):
        return '<Player {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_played = db.Column(db.Date)
    winner_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    winner_skill = db.Column(db.SmallInteger)
    winner_must_win = db.Column(db.SmallInteger)
    winner_points_won = db.Column(db.SmallInteger)
    loser_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    loser_skill = db.Column(db.SmallInteger)
    loser_must_win = db.Column(db.SmallInteger)
    loser_points_won = db.Column(db.SmallInteger)
    games = db.relationship('Game', backref='match', lazy=True)

    def __repr__(self):
        return "<Match {}, {}>".format(self.id, self.date_played)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    loser_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    innings = db.Column(db.SmallInteger, nullable=True)
    eight_on_break = db.Column(db.Boolean, nullable=True)
    winner_table_run = db.Column(db.Boolean, nullable=True)
    winner_ball_in_hands = db.Column(db.SmallInteger, nullable=True)
    loser_ball_in_hands = db.Column(db.SmallInteger, nullable=True)

    def __repr__(self):
        return "<Game {}, {}, {}, {}".format(self.id, self.match_id, 
                self.winner_id, self.loser_id)


@login.user_loader
def load_user(id):
    return Player.query.get(int(id))
