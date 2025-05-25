from app import create_app, db
from app.models.sports import SportsGame
from app.models.casino import CasinoGame
from datetime import datetime, timedelta

app = create_app()

def populate_sports_games():
    now = datetime.utcnow()
    games = [
        SportsGame(team_home='Team A', team_away='Team B', start_time=now + timedelta(hours=1), odds_home_win=1.5, odds_away_win=2.5, odds_draw=3.0),
        SportsGame(team_home='Team C', team_away='Team D', start_time=now + timedelta(hours=2), odds_home_win=1.8, odds_away_win=2.0, odds_draw=2.8),
        SportsGame(team_home='Team E', team_away='Team F', start_time=now + timedelta(hours=3), odds_home_win=2.1, odds_away_win=1.7, odds_draw=3.2)
    ]
    db.session.bulk_save_objects(games)
    db.session.commit()

def populate_casino_games():
    games = [
        CasinoGame(name='Poker', description='Classic poker game', min_bet=1.0, max_bet=500.0),
        CasinoGame(name='Blackjack', description='Beat the dealer', min_bet=1.0, max_bet=1000.0),
        CasinoGame(name='Roulette', description='Place your bets on the wheel', min_bet=0.5, max_bet=2000.0),
    ]
    db.session.bulk_save_objects(games)
    db.session.commit()

with app.app_context():
    populate_sports_games()
    populate_casino_games()
    print("Demo data populated successfully.")
