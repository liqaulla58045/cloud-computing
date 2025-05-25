from app import db
from datetime import datetime

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    balance = db.Column(db.Float, default=0.0)

    user = db.relationship('User', backref=db.backref('wallet', uselist=False))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # deposit, withdrawal, bet, win
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255))

    wallet = db.relationship('Wallet', backref=db.backref('transactions', lazy=True))
