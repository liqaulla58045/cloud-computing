from app import db
from datetime import datetime

class SportsGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_home = db.Column(db.String(100), nullable=False)
    team_away = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    odds_home_win = db.Column(db.Float, nullable=False)
    odds_away_win = db.Column(db.Float, nullable=False)
    odds_draw = db.Column(db.Float, nullable=False)

class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('sports_game.id'), nullable=False)
    bet_type = db.Column(db.String(50), nullable=False)  # home_win, away_win, draw
    amount = db.Column(db.Float, nullable=False)
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('bets', lazy=True))
    game = db.relationship('SportsGame', backref=db.backref('bets', lazy=True))
