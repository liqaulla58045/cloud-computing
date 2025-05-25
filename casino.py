from app import db

class CasinoGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    min_bet = db.Column(db.Float, default=1.0)
    max_bet = db.Column(db.Float, default=1000.0)
